import { cache } from "react";
import { auth } from "../auth";

/**
 * Cached auth session for server-side deduplication.
 * Multiple calls to getSession() within a single request
 * will only execute the auth check once.
 */
export const getSession = cache(async () => {
    return await auth();
});
