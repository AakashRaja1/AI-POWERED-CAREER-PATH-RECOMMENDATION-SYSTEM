/*
Personality storage helper. It saves and retrieves the latest personality analysis per user so recommendations can reuse recent results.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

const COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 30;

const safeEmailKey = (email) =>
  String(email || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_|_$/g, "") || "guest";

export const getCurrentUserEmail = () => {
  try {
    return localStorage.getItem("userEmail") || "";
  } catch {
    return "";
  }
};

export const buildPersonalityStorageKey = (email) => `behavior_analysis_${safeEmailKey(email)}`;
export const buildPersonalityCookieKey = (email) => `personality_traits_${safeEmailKey(email)}`;
export const buildCareerResultStorageKey = (email) => `behavior_career_result_${safeEmailKey(email)}`;
export const buildCareerResultCookieKey = (email) => `career_result_${safeEmailKey(email)}`;

const setCookie = (name, value) => {
  if (typeof document === "undefined") return;
  const encoded = encodeURIComponent(JSON.stringify(value));
  document.cookie = `${name}=${encoded}; path=/; max-age=${COOKIE_MAX_AGE_SECONDS}; samesite=lax`;
};

const getCookie = (name) => {
  if (typeof document === "undefined") return null;
  const cookie = document.cookie
    .split("; ")
    .find((entry) => entry.startsWith(`${name}=`));

  if (!cookie) return null;

  const encodedValue = cookie.slice(name.length + 1);
  try {
    return JSON.parse(decodeURIComponent(encodedValue));
  } catch {
    return null;
  }
};

export const persistPersonalityAnalysis = (email, analysis) => {
  const normalizedEmail = String(email || "").trim();
  if (!normalizedEmail) return;

  const storageKey = buildPersonalityStorageKey(normalizedEmail);
  const cookieKey = buildPersonalityCookieKey(normalizedEmail);
  const payload = {
    traits: analysis?.traits || {},
    direct_traits: analysis?.direct_traits || {},
    derived_scores: analysis?.derived_scores || {},
    score_levels: analysis?.score_levels || {},
    behavior_analysis: analysis?.behavior_analysis || {},
    meta: analysis?.meta || {},
    generated_at: analysis?.generated_at || new Date().toISOString(),
  };

  try {
    localStorage.setItem(storageKey, JSON.stringify(payload));
  } catch {
    // Ignore storage errors and still try cookies.
  }

  setCookie(cookieKey, payload);
};

export const loadPersonalityAnalysis = (email) => {
  const normalizedEmail = String(email || "").trim();
  if (!normalizedEmail) return null;

  const storageKey = buildPersonalityStorageKey(normalizedEmail);
  const cookieKey = buildPersonalityCookieKey(normalizedEmail);

  let storageValue = null;
  let cookieValue = null;

  try {
    const rawStorage = localStorage.getItem(storageKey);
    storageValue = rawStorage ? JSON.parse(rawStorage) : null;
  } catch {
    storageValue = null;
  }

  cookieValue = getCookie(cookieKey);

  if (cookieValue && storageValue) {
    return {
      ...storageValue,
      ...cookieValue,
      traits: cookieValue.traits || storageValue.traits || {},
      direct_traits: cookieValue.direct_traits || storageValue.direct_traits || {},
      derived_scores: cookieValue.derived_scores || storageValue.derived_scores || {},
      score_levels: cookieValue.score_levels || storageValue.score_levels || {},
      behavior_analysis: cookieValue.behavior_analysis || storageValue.behavior_analysis || {},
      meta: cookieValue.meta || storageValue.meta || {},
      generated_at: cookieValue.generated_at || storageValue.generated_at || new Date().toISOString(),
    };
  }

  return cookieValue || storageValue || null;
};

export const persistCareerRecommendation = (email, payload) => {
  const normalizedEmail = String(email || "").trim();
  if (!normalizedEmail) return;

  const storageKey = buildCareerResultStorageKey(normalizedEmail);
  const cookieKey = buildCareerResultCookieKey(normalizedEmail);

  try {
    localStorage.setItem(storageKey, JSON.stringify(payload));
  } catch {
    // Ignore storage errors and still try cookies.
  }

  setCookie(cookieKey, payload);
};

export const loadCareerRecommendation = (email) => {
  const normalizedEmail = String(email || "").trim();
  if (!normalizedEmail) return null;

  const storageKey = buildCareerResultStorageKey(normalizedEmail);
  const cookieKey = buildCareerResultCookieKey(normalizedEmail);

  let storageValue = null;
  let cookieValue = null;

  try {
    const rawStorage = localStorage.getItem(storageKey);
    storageValue = rawStorage ? JSON.parse(rawStorage) : null;
  } catch {
    storageValue = null;
  }

  cookieValue = getCookie(cookieKey);
  return cookieValue || storageValue || null;
};
