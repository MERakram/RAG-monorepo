import { useRagApi } from '../api/rag';
import { model, selectedCollection } from '../shared'
import type { ChatMessage } from './useHelloWorld'

// Split text into chunks to simulate streaming
function* chunkText(text: string, chunkSize: number = 10) {
  for (let i = 0; i < text.length; i += chunkSize) {
    yield text.slice(i, i + chunkSize);
  }
}

export async function* streamRagChat(messages: ChatMessage[]) {
  const { ragApi } = useRagApi();

  try {
    console.log('Using RAG service with model:', model.value);

    const lastUserMessage = [...messages]
      .filter(m => m.role === 'user')
      .pop()?.content || '';

    const payload = {
      query: lastUserMessage.trim(),
      model: model.value || undefined,
      collection_name: selectedCollection.value || undefined,
    };

    const { data } = await ragApi.chat(payload);

    console.log('Response data:', data);

    const content = typeof data === 'string' ? data : data.answer || data.response || data.message || JSON.stringify(data);

    for (const chunk of chunkText(content, 15)) {
      yield {
        content: chunk,
        delta: chunk,
        message: {
          content: chunk,
        },
      };
      await new Promise(resolve => setTimeout(resolve, 10));
    }
  } catch (error: any) {
    console.error('RAG service error:', error);
    console.error('Error details:', error.response || error);
    throw new Error(`RAG service error: ${error.message || 'Unknown error'}`);
  }
}

export async function fetchRagModels() {
  const { ragApi } = useRagApi();
  try {
    const { data } = await ragApi.getModels();
    return data.models || ['default'];
  } catch (error) {
    console.error('Error fetching RAG models:', error);
    return ['default'];
  }
}