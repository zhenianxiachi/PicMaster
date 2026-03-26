export type MotionController = {
  refresh: () => void
  destroy: () => void
}

const revealSelector = '[data-reveal]'
const staggerSelector = '[data-stagger]'
const scrubSelector = '[data-scrub]'

export const createMotionController = (): MotionController => {
  const observed = new WeakSet<Element>()
  let scrubElements: HTMLElement[] = []
  let rafId = 0

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
        }
      })
    },
    {
      root: null,
      threshold: 0.2,
      rootMargin: '0px 0px -10% 0px',
    }
  )

  const observeElement = (element: Element) => {
    if (observed.has(element)) {
      return
    }
    observed.add(element)
    observer.observe(element)
  }

  const prepareStaggerGroup = (group: Element) => {
    const children = Array.from(group.children)
    children.forEach((child, index) => {
      if (!(child instanceof HTMLElement)) {
        return
      }
      if (!child.hasAttribute('data-reveal')) {
        child.setAttribute('data-reveal', '')
      }
      child.style.setProperty('--reveal-delay', `${index * 90}ms`)
      observeElement(child)
    })
  }

  const updateScrub = () => {
    if (!scrubElements.length) {
      rafId = window.requestAnimationFrame(updateScrub)
      return
    }

    const viewport = window.innerHeight || 1
    scrubElements.forEach(element => {
      const rect = element.getBoundingClientRect()
      const progress = Math.min(1, Math.max(0, (viewport - rect.top) / (viewport + rect.height)))
      element.style.setProperty('--scrub', progress.toFixed(3))
    })

    rafId = window.requestAnimationFrame(updateScrub)
  }

  const refresh = () => {
    document.querySelectorAll(staggerSelector).forEach(prepareStaggerGroup)
    document.querySelectorAll(revealSelector).forEach(observeElement)
    scrubElements = Array.from(document.querySelectorAll(scrubSelector)).filter(
      (node): node is HTMLElement => node instanceof HTMLElement
    )
  }

  refresh()
  rafId = window.requestAnimationFrame(updateScrub)

  const destroy = () => {
    observer.disconnect()
    if (rafId) {
      window.cancelAnimationFrame(rafId)
    }
    scrubElements = []
  }

  return { refresh, destroy }
}
