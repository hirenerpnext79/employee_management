let cachedLocation = null

export const collectLogData = async () => {
  let device_type = 'Desktop'
  if (typeof navigator !== 'undefined') {
    if (navigator.userAgentData && navigator.userAgentData.mobile) {
      device_type = 'Mobile'
    } else if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '')) {
      device_type = 'Mobile'
    }
  }

  let web_code = ''
  if (typeof window !== 'undefined') {
    try {
      const searchParams = new URLSearchParams(window.location.search)
      const hashPart = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : ''
      const hashParams = new URLSearchParams(hashPart)
      web_code = (
        searchParams.get('web_code') ||
        hashParams.get('web_code') ||
        searchParams.get('token') ||
        hashParams.get('token') ||
        ''
      )
    } catch (e) {}
  }

  let data = {
    userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : '',
    language: typeof navigator !== 'undefined' ? navigator.language : '',
    platform: typeof navigator !== 'undefined' ? (navigator.userAgentData?.platform || navigator.platform || '') : '',
    device_type: device_type,
    screen: typeof window !== 'undefined' && window.screen ? `${window.screen.width}x${window.screen.height}` : '',
    referrer: typeof document !== 'undefined' ? document.referrer : '',
    url: typeof window !== 'undefined' ? window.location.href : '',
    web_code: web_code
  }

  if (cachedLocation) {
    data.location = cachedLocation
    return JSON.stringify(data)
  }

  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 2500)
    const response = await fetch('https://ipapi.co/json/', { signal: controller.signal })
    clearTimeout(timeoutId)
    if (response.ok) {
      const loc = await response.json()
      cachedLocation = loc
      data.location = loc
    }
  } catch (e) {
    // Handled gracefully
  }

  return JSON.stringify(data)
}
