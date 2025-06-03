import { model, serviceUrl } from '../shared'
import type { ChatMessage } from './useHelloWorld'
import { Ollama } from 'ollama/browser'

// Create an Ollama client instance
const getOllamaClient = () => {
  return new Ollama({
    host: serviceUrl.value
  })
}

export async function* streamOllamaChat(messages: ChatMessage[]) {
  const ollama = getOllamaClient()
  
  try {
    console.log('Using model:', model.value)
    
    // Convert our app message format to Ollama's format
    const ollamaMessages = messages
      .filter(m => m.role !== 'error')
      .map(m => ({
        role: m.role,
        content: m.content
      }))
    
    // Use Ollama's streaming API
    const stream = await ollama.chat({
      model: model.value,
      messages: ollamaMessages,
      stream: true
    })
    
    // Yield each chunk from the stream
    for await (const part of stream) {
      // console.log('Stream chunk:', part)
      yield {
        content: part.message?.content || '',
        // Include other properties for compatibility
        delta: part.message?.content || '',
        message: {
          content: part.message?.content || ''
        }
      }
    }
  } catch (error: any) {
    console.error('Ollama chat error:', error)
    throw new Error(`Ollama API error: ${error.message || 'Unknown error'}`)
  }
}

export async function fetchOllamaModels() {
  const ollama = getOllamaClient()
  
  try {
    // Use Ollama's models API
    const response = await ollama.list()
    return response.models.map(model => model.name)
  } catch (error) {
    console.error('Error fetching Ollama models:', error)
    return []
  }
}