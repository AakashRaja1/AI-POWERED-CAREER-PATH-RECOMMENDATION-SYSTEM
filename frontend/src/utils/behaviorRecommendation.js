/*
Rule-based behavior recommendation helper. It converts personality and behavior signals into career hints when a lightweight local recommendation is needed.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

const GENERIC_TOKENS = new Set([
  "step",
  "steps",
  "duration",
  "time",
  "timeline",
  "resource",
  "resources",
  "notes",
  "note",
  "resources & tools",
  "resources/tools",
]);

const normalizeItemText = (value) =>
  String(value || "")
    .replace(/^\s*(?:[-*•]|\d+[.)\-:]?)\s*/, "")
    .replace(/\s+/g, " ")
    .trim();

const isGenericToken = (value) => {
  const normalized = normalizeItemText(value).toLowerCase().replace(/[:.-]+$/g, "");
  return !normalized || GENERIC_TOKENS.has(normalized) || /^step\s*\d*$/i.test(normalized);
};

const splitToList = (value) => {
  if (Array.isArray(value)) {
    const cleaned = [];
    for (let i = 0; i < value.length; i += 1) {
      const current = normalizeItemText(value[i]);
      if (!current) continue;

      const currentLower = current.toLowerCase();
      if (isGenericToken(current)) {
        const next = normalizeItemText(value[i + 1]);
        if (next && !isGenericToken(next)) {
          if (currentLower === "duration" || currentLower === "timeline") {
            cleaned.push(`Duration: ${next}`);
          } else if (currentLower === "resource" || currentLower === "resources") {
            const resources = [next];
            let cursor = i + 2;
            while (cursor < value.length) {
              const extra = normalizeItemText(value[cursor]);
              if (!extra || isGenericToken(extra)) break;
              resources.push(extra);
              cursor += 1;
            }
            cleaned.push(`Resources: ${resources.join("; ")}`);
            i = cursor - 1;
          } else {
            cleaned.push(next);
          }
          i += 1;
        }
        continue;
      }

      cleaned.push(current);
    }
    return [...new Set(cleaned)].filter(Boolean);
  }
  if (typeof value === "string") {
    const parts = value
      .split(/\n|\r|;|,|\u2022/g)
      .map((item) => normalizeItemText(item))
      .filter(Boolean);

    return splitToList(parts);
  }
  return [];
};

const parseConfidence = (value) => {
  if (typeof value === "number" && Number.isFinite(value)) {
    return Math.max(0, Math.min(1, value));
  }

  const match = String(value ?? "").match(/[-+]?\d*\.?\d+/);
  if (!match) return 0;

  const n = Number(match[0]);
  if (!Number.isFinite(n)) return 0;
  return Math.max(0, Math.min(1, n));
};

const deriveConfidence = (recommendation) => {
  const signalCount = [
    recommendation.career_path,
    recommendation.rationale,
    ...(recommendation.best_fit_roles || []),
    ...(recommendation.skills_to_build || []),
    ...(recommendation.roadmap || []),
  ].filter(Boolean).length;

  const score = 0.58 + Math.min(0.28, signalCount * 0.012);
  return Math.max(0.58, Math.min(0.88, score));
};

const extractEmbeddedJson = (text) => {
  if (typeof text !== "string") return null;
  const trimmed = text.trim();
  if (!trimmed) return null;

  try {
    const parsed = JSON.parse(trimmed);
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch {
    // no-op
  }

  const fenced = trimmed.match(/```(?:json)?\s*(\{[\s\S]*?\})\s*```/i);
  if (fenced?.[1]) {
    try {
      const parsed = JSON.parse(fenced[1]);
      return parsed && typeof parsed === "object" ? parsed : null;
    } catch {
      // no-op
    }
  }

  const start = trimmed.indexOf("{");
  const end = trimmed.lastIndexOf("}");
  if (start !== -1 && end > start) {
    const candidate = trimmed.slice(start, end + 1);
    try {
      const parsed = JSON.parse(candidate);
      return parsed && typeof parsed === "object" ? parsed : null;
    } catch {
      // no-op
    }
  }

  return null;
};

export const normalizeBehaviorRecommendation = (input) => {
  const base = input && typeof input === "object" ? input : {};
  const embedded = extractEmbeddedJson(base.rationale);
  const merged = embedded && typeof embedded === "object" ? { ...embedded, ...base } : base;

  const recommendation = {
    career_path: String(merged.career_path || "").trim() || "Career recommendation",
    rationale: String(merged.rationale || "").trim(),
    best_fit_roles: splitToList(merged.best_fit_roles),
    skills_to_build: splitToList(merged.skills_to_build),
    roadmap: splitToList(merged.roadmap),
    confidence: parseConfidence(merged.confidence),
  };

  if (!recommendation.confidence && recommendation.career_path !== "Career recommendation") {
    recommendation.confidence = deriveConfidence(recommendation);
  }

  return recommendation;
};
