import { NextRequest, NextResponse } from "next/server";
import { OllamaGeneration } from "@/lib/llm-generation";
import { Claim } from "@/database/queries";

/**
 * Handles POST requests to generate a tag for a customer claim using an LLM.
 * 
 * @param {NextRequest} request - The incoming Next.js request object containing the claim data.
 * @returns {Promise<NextResponse>} A promise that resolves to a NextResponse containing the generated tagId or an error status.
 */
export async function POST(request: NextRequest) {
  try {
    const { claim }: { claim: Claim } = await request.json();

    const response = await OllamaGeneration(claim);

    return NextResponse.json({ tagId: response }, { status: 200 });
  } catch (error) {
    console.error(error);
  }
}
