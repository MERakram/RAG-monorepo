import { nextTick, onBeforeUnmount, ref } from 'vue'

export function useScrollToBottom(containerRef: Ref<HTMLElement | null>, scrollThreshold = 50, enable: MaybeRef<boolean> = true) {

  const isStickToBottom = ref(false)

  const lastContentHeight = ref(0)

  const isNearBottom = (): boolean => {
    if (!containerRef.value) {
      return false
    }

    const { scrollTop, scrollHeight, clientHeight } = containerRef.value

    const distanceToBottom = scrollHeight - scrollTop - clientHeight

    return distanceToBottom <= scrollThreshold
  }

  const scrollToBottom = () => {
    if (!containerRef.value || !unref(enable)) {
      return
    }
    containerRef.value.scrollTop = containerRef.value.scrollHeight
  }

  const handleScroll = () => {
    if (!containerRef.value) {
      return
    }

    if (isNearBottom()) {
      isStickToBottom.value = true
    }
    else {
      isStickToBottom.value = false
    }
  }

  const observeContentChange = () => {
    if (!containerRef.value) {
      return
    }

    const observer = new MutationObserver(async () => {
      if (!containerRef.value) {
        return
      }

      await nextTick()

      const { scrollHeight } = containerRef.value

      if (scrollHeight > lastContentHeight.value && isStickToBottom.value) {
        scrollToBottom()
      }

      lastContentHeight.value = scrollHeight
    })

    observer.observe(containerRef.value, {
      childList: true,
      subtree: true,
      characterData: true,
    })

    return observer
  }

  let observer = observeContentChange()
  watch([containerRef], () => {
    if (containerRef.value) {
      containerRef.value.addEventListener('scroll', handleScroll)

      observer = observeContentChange()

      lastContentHeight.value = containerRef.value.scrollHeight

      scrollToBottom()
    }
  })

  onBeforeUnmount(() => {
    if (containerRef.value) {
      containerRef.value.removeEventListener('scroll', handleScroll)
    }

    if (observer) {
      observer.disconnect()
    }
  })
}
