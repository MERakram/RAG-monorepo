import { client, serviceUrl, platform } from '../shared'


export function useClient() {
  return client
}

export const ollamaUrl = computed(() => {
  if (platform.value === 'ollama') {
    return serviceUrl.value
  }
  return ''
})

// export async function fetchOllamaModels() {
//   try {
//     const response = await fetch(`${ollamaUrl.value}/api/tags`)
//     const data = await response.json()
//     if (data && data.models) {
//       return data.models.map((model: any) => model.name)
//     }
//     return []
//   } catch (error) {
//     console.error('Error fetching Ollama models:', error)
//     return []
//   }
// }

export function useModels() {
  const models = ref<string[]>([])
  
  onMounted(async () => {
    try {
      if (platform.value === 'ollama') {
        models.value = await fetchOllamaModels()
      } else if (platform.value === 'rag'){
        models.value = await fetchRagModels()
      }else  {
        const response = await client.value.models.list()
        models.value = response.data.map(d => d.id)
      }
    }
    catch (error) {
      console.error(error)
    }
  })
  
  watch(client, async () => {
    try {
      if (platform.value === 'ollama') {
        models.value = await fetchOllamaModels()
      } else if (platform.value === 'rag'){
        models.value = await fetchRagModels()
      }else {
        const response = await client.value.models.list()
        models.value = response.data.map(d => d.id)
      }
    }
    catch (error) {
      console.error(error)
    }
  })
  
  return models
}
