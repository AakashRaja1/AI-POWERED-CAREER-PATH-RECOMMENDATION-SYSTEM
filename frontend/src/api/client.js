const API_CANDIDATES = [
  "/api",
  "http://127.0.0.1:8000",
  "http://localhost:8000",
];

function withTimeout(ms = 30000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), ms);
  return { controller, timeoutId };
}

async function readErrorResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    const data = await response.json();
    if (typeof data?.detail === "string") return data.detail;
    return JSON.stringify(data);
  }
  return await response.text();
}

export async function postWithFallback(path, body, options = {}) {
  const { timeoutMs = 45000 } = options;
  let lastError = null;

  for (const base of API_CANDIDATES) {
    const { controller, timeoutId } = withTimeout(timeoutMs);

    try {
      const response = await fetch(`${base}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorText = await readErrorResponse(response);
        throw new Error(errorText || `Request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      lastError = error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  if (lastError?.name === "AbortError") {
    throw new Error("Request timed out. Please try again.");
  }

  if (String(lastError?.message || "").toLowerCase().includes("failed to fetch")) {
    throw new Error("Unable to reach backend API. Start backend server on port 8000 and try again.");
  }

  throw lastError || new Error("Unable to complete request.");
}
