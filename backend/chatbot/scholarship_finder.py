"""
Scholarship matching helper. It searches scholarship data and formats relevant funding opportunities for the user.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import json
import logging
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import requests
from bs4 import BeautifulSoup

from app.core.config import settings
from .groq_client import get_groq_client

logger = logging.getLogger(__name__)

SCHOLARSHIP_KEYWORDS = (
    "scholarship",
    "fellowship",
    "grant",
    "funded",
    "financial aid",
    "tuition",
    "daad",
)

NOISE_KEYWORDS = (
    "kahoot",
    "multiplication",
    "game-based",
    "trivia",
    "mobile app",
    "play kahoot",
)

LLM_MAX_CONTEXT_RESULTS = 2
SEARCH_TIMEOUT_SECONDS = 10
PAGE_TIMEOUT_SECONDS = 8


def _searxng_instances() -> list[str]:
    raw = settings.SEARXNG_BASE_URLS or settings.SEARXNG_BASE_URL
    instances = [part.strip().rstrip("/") for part in raw.split(",") if part.strip()]
    return instances or ["https://searx.be"]


def _searxng_search(query: str, max_results: int = 10) -> list[dict[str, str]]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    for base_url in _searxng_instances():
        search_url = f"{base_url}/search"
        try:
            response = requests.get(
                search_url,
                params={
                    "q": query,
                    "format": "json",
                    "language": "en",
                    "safesearch": 1,
                },
                headers=headers,
                timeout=settings.SEARXNG_REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            payload = response.json()
            raw_results = payload.get("results", [])

            parsed: list[dict[str, str]] = []
            for item in raw_results:
                url = (item.get("url") or "").strip()
                title = " ".join((item.get("title") or "").split())
                snippet = " ".join((item.get("content") or "").split())
                if not url or not title:
                    continue

                parsed.append({"title": title, "url": url, "snippet": snippet})
                if len(parsed) >= max_results:
                    break

            if parsed:
                logger.info("SearxNG search succeeded using %s", base_url)
                return parsed
        except Exception as exc:
            logger.debug("SearxNG search unavailable for %s: %s", base_url, exc)

    return []


def _decode_duckduckgo_redirect(raw_url: str) -> str:
    if "duckduckgo.com/l/?" not in raw_url:
        return raw_url

    parsed = urlparse(raw_url)
    query = parse_qs(parsed.query)
    target = query.get("uddg", [raw_url])[0]
    return unquote(target)


def _decode_bing_redirect(raw_url: str) -> str:
    if "bing.com/ck/a" not in raw_url:
        return raw_url

    parsed = urlparse(raw_url)
    query = parse_qs(parsed.query)
    target = query.get("u", [raw_url])[0]

    # Bing commonly prefixes URLs with a1.
    if target.startswith("a1"):
        target = target[2:]

    try:
        decoded = unquote(target)
        return decoded if decoded.startswith("http") else raw_url
    except Exception:
        return raw_url


def _is_probably_scholarship_result(title: str, snippet: str, url: str) -> bool:
    blob = " ".join([title, snippet, url]).lower()

    if any(noise in blob for noise in NOISE_KEYWORDS):
        return False

    return any(keyword in blob for keyword in SCHOLARSHIP_KEYWORDS)


def _strip_html_text(page_html: str, max_chars: int = 3000) -> str:
    try:
        soup = BeautifulSoup(page_html, "html.parser")
        for tag in soup.find_all(["script", "style", "noscript"]):
            tag.decompose()
        text = " ".join(soup.get_text(" ").split())
        return text[:max_chars]
    except Exception:
        return ""


def _duckduckgo_search(query: str, max_results: int = 10) -> list[dict[str, str]]:
    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    response = requests.get(url, params={"q": query}, headers=headers, timeout=SEARCH_TIMEOUT_SECONDS)
    if response.status_code >= 300:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results: list[dict[str, str]] = []

    for node in soup.select("div.result"):
        link_node = node.select_one("a.result__a")
        if not link_node:
            continue

        raw_href = (link_node.get("href") or "").strip()
        if not raw_href:
            continue

        title = " ".join(link_node.get_text(" ").split())
        source_url = _decode_duckduckgo_redirect(raw_href)

        snippet_node = node.select_one("a.result__snippet, div.result__snippet")
        snippet = " ".join(snippet_node.get_text(" ").split()) if snippet_node else ""

        results.append(
            {
                "title": title,
                "url": source_url,
                "snippet": snippet,
            }
        )

        if len(results) >= max_results:
            break

    return results
def _bing_search(query: str, max_results: int = 10) -> list[dict[str, str]]:
    url = "https://www.bing.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    response = requests.get(url, params={"q": query}, headers=headers, timeout=SEARCH_TIMEOUT_SECONDS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results: list[dict[str, str]] = []

    for node in soup.select("li.b_algo"):
        link_node = node.select_one("h2 a")
        if not link_node:
            continue

        source_url = _decode_bing_redirect((link_node.get("href") or "").strip())
        title = " ".join(link_node.get_text(" ").split())
        if not source_url or not title:
            continue

        snippet_node = node.select_one("div.b_caption p")
        snippet = " ".join(snippet_node.get_text(" ").split()) if snippet_node else ""

        results.append(
            {
                "title": title,
                "url": source_url,
                "snippet": snippet,
            }
        )

        if len(results) >= max_results:
            break

    return results


def _web_search(query: str, max_results: int = 10, prefer_searxng: bool = False) -> list[dict[str, str]]:
    if prefer_searxng:
        searx_results = _searxng_search(query=query, max_results=max_results)
        if searx_results:
            return searx_results

        logger.debug("SearxNG returned no results, falling back to DuckDuckGo/Bing")

    try:
        ddg_results = _duckduckgo_search(query=query, max_results=max_results)
        if ddg_results:
            return ddg_results
    except Exception as exc:
        logger.warning("DuckDuckGo search failed: %s", exc)

    logger.debug("DuckDuckGo returned no results, falling back to Bing search")
    try:
        return _bing_search(query=query, max_results=max_results)
    except Exception as exc:
        logger.warning("Bing search failed: %s", exc)
        return []


def _search_multiple_queries(queries: list[str], max_results: int = 10) -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for query_index, query in enumerate(queries):
        use_searxng = query_index == 0
        for item in _web_search(
            query=query,
            max_results=max_results,
            prefer_searxng=use_searxng,
        ):
            url = item.get("url", "")
            if not url or url in seen_urls:
                continue

            seen_urls.add(url)
            if _is_probably_scholarship_result(
                title=item.get("title", ""),
                snippet=item.get("snippet", ""),
                url=url,
            ):
                merged.append(item)

            if len(merged) >= max_results:
                return merged

    return merged


def _fetch_source_context(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    try:
        response = requests.get(url, headers=headers, timeout=PAGE_TIMEOUT_SECONDS)
        response.raise_for_status()
        return _strip_html_text(response.text, max_chars=1200)
    except Exception as exc:
        logger.warning("Could not fetch source %s: %s", url, exc)
        return ""


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        maybe_json = text[start : end + 1]
        return json.loads(maybe_json)

    raise ValueError("Model did not return valid JSON")


def _build_query(
    degree_level: str,
    field_of_study: str,
    country: str,
    university_type: str,
    funding_type: str,
) -> str:
    return (
        f"{funding_type} {degree_level} scholarships in {country} "
        f"for {field_of_study} students {university_type} universities"
    )


def _fallback_sources_for_country(country: str) -> list[dict[str, str]]:
    country_key = (country or "").strip().lower()
    common = [
        {
            "title": "ScholarshipPortal - International Scholarships",
            "url": "https://www.scholarshipportal.com/",
            "snippet": "Search scholarships by country, degree level, and field.",
        },
        {
            "title": "Opportunity Desk - Scholarships",
            "url": "https://opportunitydesk.org/category/scholarships/",
            "snippet": "Regularly updated scholarship opportunities worldwide.",
        },
        {
            "title": "WeMakeScholars Scholarships",
            "url": "https://www.wemakescholars.com/scholarships",
            "snippet": "Scholarship listings filtered by study destination and degree.",
        },
    ]

    country_specific = {
        "germany": [
            {
                "title": "DAAD Scholarship Database",
                "url": "https://www.daad.de/en/studying-in-germany/scholarships/",
                "snippet": "Official DAAD funding and scholarship search.",
            }
        ],
        "usa": [
            {
                "title": "EducationUSA Financial Aid",
                "url": "https://educationusa.state.gov/",
                "snippet": "Official U.S. government-supported study guidance and funding resources.",
            }
        ],
        "canada": [
            {
                "title": "EduCanada Scholarships",
                "url": "https://www.educanada.ca/scholarships-bourses/index.aspx?lang=eng",
                "snippet": "Official Canadian scholarship opportunities for international students.",
            }
        ],
        "uk": [
            {
                "title": "Chevening Scholarships",
                "url": "https://www.chevening.org/",
                "snippet": "Fully funded UK government scholarships for postgraduate study.",
            }
        ],
        "united kingdom": [
            {
                "title": "Chevening Scholarships",
                "url": "https://www.chevening.org/",
                "snippet": "Fully funded UK government scholarships for postgraduate study.",
            }
        ],
        "australia": [
            {
                "title": "Australia Awards",
                "url": "https://www.australiaawards.gov.au/",
                "snippet": "Official Australian government scholarship program.",
            }
        ],
    }

    return country_specific.get(country_key, []) + common


def _fallback_scholarship_entries(
    *,
    degree_level: str,
    field_of_study: str,
    country: str,
    university_type: str,
    funding_type: str,
    max_results: int,
    sources: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    source_items = sources or _fallback_sources_for_country(country)
    scholarships: list[dict[str, Any]] = []

    for source in source_items[:max_results]:
        source_url = (source.get("url") or "").strip()
        scholarships.append(
            {
                "university_name": "Not clearly specified",
                "scholarship_name": source.get("title") or "Scholarship Opportunity",
                "degree_level": degree_level,
                "field_of_study": field_of_study,
                "country": country,
                "university_type": university_type,
                "funding_type": funding_type,
                "stipend": "Not clearly specified",
                "tuition_coverage": "Not clearly specified",
                "deadline": "Check official source",
                "requirements": ["Refer to official scholarship page"],
                "documents_needed": ["Academic profile", "Academic transcripts", "Statement of purpose"],
                "application_process": "Open the official link and follow the scholarship-specific process.",
                "application_link": source_url,
                "source_link": source_url,
                "notes": source.get("snippet") or "Fallback scholarship source.",
            }
        )

    return scholarships[:max_results]


def find_scholarships(
    degree_level: str,
    field_of_study: str,
    country: str,
    university_type: str,
    funding_type: str,
    max_results: int = 10,
) -> dict[str, Any]:
    query = _build_query(
        degree_level=degree_level,
        field_of_study=field_of_study,
        country=country,
        university_type=university_type,
        funding_type=funding_type,
    )

    queries = [
        query,
        f"{degree_level} {field_of_study} scholarships {country}",
        f"{funding_type} scholarships {country} {degree_level} {field_of_study}",
    ]

    search_results = _search_multiple_queries(queries=queries, max_results=max_results)

    if not search_results:
        fallback_sources = _fallback_sources_for_country(country)
        fallback_scholarships = _fallback_scholarship_entries(
            degree_level=degree_level,
            field_of_study=field_of_study,
            country=country,
            university_type=university_type,
            funding_type=funding_type,
            max_results=max_results,
            sources=fallback_sources,
        )
        return {
            "summary": "Live search returned no direct results, so we provided trusted scholarship portals you can use immediately.",
            "search_query": query,
            "scholarships": fallback_scholarships,
            "checklist": [
                "Open each source link and filter by degree, field, and destination country.",
                "Verify eligibility and deadlines on official pages.",
                "Prepare core documents before applying.",
            ],
            "sources": fallback_sources,
        }

    source_context_blocks: list[str] = []
    for idx, result in enumerate(search_results[:LLM_MAX_CONTEXT_RESULTS], start=1):
        source_block = (
            f"SOURCE {idx}\n"
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['snippet']}\n"
        )
        if len(search_results) <= 2 and idx == 1:
            page_context = _fetch_source_context(result["url"])
            if page_context:
                source_block += f"Page Context: {page_context}\n"
        source_context_blocks.append(source_block)

    llm_prompt = f"""
You are a scholarship research assistant.

User Preferences:
- Degree Level: {degree_level}
- Field of Study: {field_of_study}
- Target Country: {country}
- University Type: {university_type}
- Funding Type: {funding_type}

Below are web search results and extracted page context. Use only this evidence.
Do not fabricate scholarships or links.

{chr(10).join(source_context_blocks)}

Return strict JSON with this shape:
{{
  "summary": "short paragraph",
  "scholarships": [
    {{
      "university_name": "",
      "scholarship_name": "",
      "degree_level": "",
      "field_of_study": "",
      "country": "",
      "university_type": "",
      "funding_type": "",
      "stipend": "",
      "tuition_coverage": "",
      "deadline": "",
      "requirements": [""],
      "documents_needed": [""],
      "application_process": "",
      "application_link": "",
      "source_link": "",
      "notes": ""
    }}
  ],
  "checklist": ["actionable next step"]
}}

Rules:
- Return up to {max_results} scholarships.
- If a detail is not available, write "Not clearly specified".
- Ensure source_link and application_link are valid URLs from the given sources when possible.
"""

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model=settings.GROQ_CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You produce accurate scholarship research in JSON. Be concise."},
                {"role": "user", "content": llm_prompt},
            ],
            temperature=0.1,
            max_tokens=min(settings.GROQ_MAX_COMPLETION_TOKENS, 700),
        )

        response_text = completion.choices[0].message.content or "{}"
        structured = _extract_json(response_text)
    except Exception as exc:
        logger.warning("Falling back to source-based scholarship results due to LLM failure: %s", exc)
        fallback_scholarships = _fallback_scholarship_entries(
            degree_level=degree_level,
            field_of_study=field_of_study,
            country=country,
            university_type=university_type,
            funding_type=funding_type,
            max_results=max_results,
            sources=search_results,
        )
        return {
            "summary": "Showing source-based scholarship opportunities because AI structuring is currently unavailable.",
            "search_query": query,
            "scholarships": fallback_scholarships,
            "checklist": [
                "Review each source link and shortlist matching opportunities.",
                "Confirm funding coverage and application deadlines.",
                "Apply through official scholarship portals only.",
            ],
            "sources": search_results,
        }

    scholarships = structured.get("scholarships")
    if not isinstance(scholarships, list):
        scholarships = []

    # Guarantee a consistent response size by filling with evidence-backed fallback entries.
    # This avoids fabricating data while still returning at least the requested count when sources exist.
    if len(scholarships) < max_results:
        used_links = {
            (item.get("source_link") or item.get("application_link") or "").strip().lower()
            for item in scholarships
            if isinstance(item, dict)
        }

        for source in search_results:
            source_url = (source.get("url") or "").strip()
            if not source_url or source_url.lower() in used_links:
                continue

            scholarships.append(
                {
                    "university_name": "Not clearly specified",
                    "scholarship_name": source.get("title") or "Scholarship Opportunity",
                    "degree_level": degree_level,
                    "field_of_study": field_of_study,
                    "country": country,
                    "university_type": university_type,
                    "funding_type": funding_type,
                    "stipend": "Not clearly specified",
                    "tuition_coverage": "Not clearly specified",
                    "deadline": "Not clearly specified",
                    "requirements": ["Not clearly specified"],
                    "documents_needed": ["Not clearly specified"],
                    "application_process": "Refer to source link for official process.",
                    "application_link": source_url,
                    "source_link": source_url,
                    "notes": source.get("snippet") or "Derived from search source.",
                }
            )
            used_links.add(source_url.lower())
            if len(scholarships) >= max_results:
                break

    structured["scholarships"] = scholarships[:max_results]
    structured["search_query"] = query
    structured["sources"] = search_results
    return structured
