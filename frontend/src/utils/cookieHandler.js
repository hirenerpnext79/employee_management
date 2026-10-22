export const setCookie = (name, value, days = 3650) => {
  if (typeof document === 'undefined') return
  const date = new Date()
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000)
  const expires = '; expires=' + date.toUTCString()
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value || '')}${expires}; path=/; SameSite=Lax`
}

export const getCookie = (name) => {
  if (typeof document === 'undefined') return ''
  const nameEQ = encodeURIComponent(name) + '='
  const ca = document.cookie.split(';')
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim()
    if (c.indexOf(nameEQ) === 0) {
      return decodeURIComponent(c.substring(nameEQ.length))
    }
  }
  return ''
}

export const deleteCookie = (name) => {
  if (typeof document === 'undefined') return
  document.cookie = `${encodeURIComponent(name)}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Lax`
}

export const setFeedbackContact = (email, mobile) => {
  if (email) {
    setCookie('hns_feedback_email', email)
    try {
      localStorage.setItem('hns_feedback_email', email)
    } catch (e) {}
  }
  if (mobile !== undefined && mobile !== null) {
    setCookie('hns_feedback_mobile', mobile)
    try {
      localStorage.setItem('hns_feedback_mobile', mobile)
    } catch (e) {}
  }
}

export const getFeedbackContact = () => {
  let email = getCookie('hns_feedback_email')
  if (!email) {
    try {
      email = localStorage.getItem('hns_feedback_email') || ''
    } catch (e) {}
  }
  let mobile = getCookie('hns_feedback_mobile')
  if (!mobile) {
    try {
      mobile = localStorage.getItem('hns_feedback_mobile') || ''
    } catch (e) {}
  }
  return { email, mobile }
}

const purgeObsoleteStorageKeys = () => {
  if (typeof window === 'undefined') return
  const preserveKeys = new Set([
    'hns_session_token',
    'hns_logged_user',
    'hns_pwd_global',
    'hns_user_data',
    'hns_web_code',
    'hns_feedback_email',
    'hns_feedback_mobile'
  ])
  const obsoletePatterns = [/^hns_session_.+/, /^hns_user_.+/, /^hns_pwd_.+/, /^hns_req_pwd_.+/]
  const cleanStorage = (storage) => {
    try {
      const toRemove = []
      for (let i = 0; i < storage.length; i++) {
        const k = storage.key(i)
        if (k && !preserveKeys.has(k) && obsoletePatterns.some(p => p.test(k))) {
          toRemove.push(k)
        }
      }
      toRemove.forEach(k => storage.removeItem(k))


    } catch (e) {}
  }
  cleanStorage(localStorage)
  cleanStorage(sessionStorage)
}

purgeObsoleteStorageKeys()

export const getGlobalSessionToken = () => {
  let token = ''
  try {
    token = localStorage.getItem('hns_session_token') || sessionStorage.getItem('hns_session_token') || getCookie('hns_session_token') || ''
  } catch (e) {
    token = getCookie('hns_session_token') || ''
  }
  return token || ''
}

export const setGlobalSession = (sessionToken, userObjOrName = null, password = '') => {
  if (!sessionToken) return

  setCookie('hns_session_token', sessionToken, 30)
  try {
    localStorage.setItem('hns_session_token', sessionToken)
    sessionStorage.setItem('hns_session_token', sessionToken)
  } catch (e) {}

  const effectiveUser = userObjOrName || getGlobalUserData() || getGlobalUser()
  if (effectiveUser) {
    let nameStr = ''
    let dataObj = null
    if (typeof effectiveUser === 'object' && effectiveUser !== null) {
      dataObj = effectiveUser
      nameStr = effectiveUser.user_name || effectiveUser.email || effectiveUser.name || ''
    } else if (typeof effectiveUser === 'string') {
      nameStr = effectiveUser
      dataObj = { user_name: nameStr }
    }

    if (dataObj) {
      try {
        const jsonStr = JSON.stringify(dataObj)
        localStorage.setItem('hns_user_data', jsonStr)
        sessionStorage.setItem('hns_user_data', jsonStr)
      } catch (e) {}
    }

    if (nameStr) {
      try {
        localStorage.setItem('hns_logged_user', nameStr)
        sessionStorage.setItem('hns_logged_user', nameStr)
      } catch (e) {}
    }
  }

  const effectivePwd = password || getGlobalPassword()
  if (effectivePwd) {
    try {
      localStorage.setItem('hns_pwd_global', effectivePwd)
      sessionStorage.setItem('hns_pwd_global', effectivePwd)
    } catch (e) {}
  }
}

export const getGlobalUser = () => {
  try {
    const user = localStorage.getItem('hns_logged_user') || sessionStorage.getItem('hns_logged_user')
    if (user) return user
  } catch (e) {}

  const userData = getGlobalUserData()
  if (userData && (userData.user_name || userData.email)) {
    return userData.user_name || userData.email
  }

  return ''
}

export const getGlobalUserData = () => {
  try {
    const raw = localStorage.getItem('hns_user_data') || sessionStorage.getItem('hns_user_data')
    if (raw) return JSON.parse(raw)
  } catch (e) {}
  return null
}

export const getGlobalPassword = () => {
  try {
    return sessionStorage.getItem('hns_pwd_global') || localStorage.getItem('hns_pwd_global') || ''
  } catch (e) {}
  return ''
}

export const clearGlobalSession = () => {
  deleteCookie('hns_session_token')

  const targetPrefixes = ['hns_session', 'hns_user', 'hns_pwd', 'hns_req_pwd', 'hns_logged', 'hns_page', 'hns_web']

  const clearStorage = (storage) => {
    try {
      const keysToRemove = []
      for (let i = 0; i < storage.length; i++) {
        const key = storage.key(i)
        if (key && targetPrefixes.some(prefix => key.startsWith(prefix))) {
          if (key !== 'hns_feedback_email' && key !== 'hns_feedback_mobile') {
            keysToRemove.push(key)
          }
        }
      }
      keysToRemove.forEach(k => storage.removeItem(k))
    } catch (e) {}
  }

  clearStorage(localStorage)
  clearStorage(sessionStorage)
}

export const clearStoredWebCode = () => {
  try {
    sessionStorage.removeItem('hns_web_code')
    localStorage.removeItem('hns_web_code')
  } catch (e) {}
}

export const setStoredWebCode = (webCode) => {
  if (!webCode) {
    clearStoredWebCode()
    return
  }
  const cleanCode = String(webCode).trim()
  if (!cleanCode) {
    clearStoredWebCode()
    return
  }
  try {
    sessionStorage.setItem('hns_web_code', cleanCode)
    localStorage.setItem('hns_web_code', cleanCode)
  } catch (e) {}
}

export const getStoredWebCode = () => {
  try {
    return sessionStorage.getItem('hns_web_code') || localStorage.getItem('hns_web_code') || ''
  } catch (e) {}
  return ''
}

