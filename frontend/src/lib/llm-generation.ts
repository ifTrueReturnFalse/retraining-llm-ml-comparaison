import { Claim } from "@/database/queries";
import { Ollama } from "ollama";
import { ALLOWED_TAGS } from "@/constants/tags";

export async function OllamaGeneration(claim: Claim) {
  const ollama = new Ollama();

  const numberedTags = ALLOWED_TAGS.map((tag, index) => `${index}. ${tag}`).join('\n')

  const response = await ollama.generate({
    model: "mistral:7b",
    prompt: `
    ROLE: You are a highly precise Customer Support Classifier. Your sole purpose is to map customer complaints to a specific predefined tag.
    
    INSTRUCTION :
    Analyze the customer complaint and select the most appropriate tag number from the list below.

    CONSTRAINTS :
    - Output ONLY the tag tex.
    - Output must EXACTLY macth one tag number from the list.
    - No explanations, no punctuation, no extra words.
    - If unsure, pick the closest tag number.
    - Never invent a new tag number.

    ALLOWED TAGS LIST :
    ${numberedTags}

    COMPLAINT DETAILS : 
    ${claim.content}

    IMPORTANT :
    Before answering, internally verify that your output is in the list.

    ANSWER :`,
  });

  return CheckLLMResponse(parseInt(response.response));
}

function CheckLLMResponse(response: number) {
  if (response <= 0 && response < ALLOWED_TAGS.length) {
    throw new Error("Réponse LLM incorrecte !");
  }

  return response;
}
