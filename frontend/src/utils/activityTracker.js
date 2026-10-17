export const collectLogData = async () => {
  let device_type = 'Desktop'
  if (typeof navigator !== 'undefined') {
    if (navigator.userAgentData && navigator.userAgentData.mobile) {
      device_type = 'Mobile'
    } else if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '')) {
      device_type = 'Mobile'
    }
  }

  let data = {
    userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : '',
    language: typeof navigator !== 'undefined' ? navigator.language : '',
    platform: typeof navigator !== 'undefined' ? (navigator.userAgentData?.platform || navigator.platform || '') : '',
    device_type: device_type,
    screen: typeof window !== 'undefined' && window.screen ? `${window.screen.width}x${window.screen.height}` : '',
    referrer: typeof document !== 'undefined' ? document.referrer : ''
  }

  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 2500)
    const response = await fetch('https://ipapi.co/json/', { signal: controller.signal })
    clearTimeout(timeoutId)
    if (response.ok) {
      const loc = await response.json()
      data.location = loc
    }
  } catch (e) {
    // Handled gracefully
  }

  return JSON.stringify(data)
}
