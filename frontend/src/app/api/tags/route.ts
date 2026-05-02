import { NextRequest, NextResponse } from "next/server";
import { Claim } from "@/database/queries";

export async function POST(request: NextRequest) {
  try {
    const { claim }: { claim: Claim } = await request.json();

    const response = await fetch("http://localhost:8000/tag", {
      method: "POST",
      body: JSON.stringify({ user_claim: claim.content }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    return NextResponse.json(
      { prediction: result.prediction },
      { status: 200 },
    );
  } catch (error) {
    console.error(error);
  }
}
