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
