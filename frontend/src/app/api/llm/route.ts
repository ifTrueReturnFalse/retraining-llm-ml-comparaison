import { NextRequest, NextResponse } from "next/server";
import { OllamaGeneration } from "@/lib/llm-generation";
import { Claim } from "@/database/queries";

export async function POST(request: NextRequest) {
  try {
    const { claim }: { claim: Claim } = await request.json();
    console.log("Start LLM generation");
    const response = await OllamaGeneration(claim);
    console.log(response);
    return NextResponse.json({ tagId: response }, { status: 200 });
  } catch (error) {
    console.error(error);
  }
}
