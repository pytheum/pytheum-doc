import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Cache the upstream response for 60s so we don't hammer api.pytheum.com.
export const revalidate = 60;

const PYTHEUM_API_BASE =
  process.env.PYTHEUM_API_BASE ?? "https://api.pytheum.com";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q") ?? searchParams.get("query");
  if (!query) {
    return NextResponse.json(
      { detail: "missing required query param: q" },
      { status: 400 },
    );
  }

  const limit = searchParams.get("limit") ?? "5";
  const upstream = new URL("/v1/markets/relevant-to", PYTHEUM_API_BASE);
  upstream.searchParams.set("query", query);
  upstream.searchParams.set("limit", limit);

  const res = await fetch(upstream, { next: { revalidate: 60 } });
  if (!res.ok) {
    return NextResponse.json(
      { detail: `upstream ${res.status}` },
      { status: res.status },
    );
  }
  const data = await res.json();
  return NextResponse.json(data);
}
