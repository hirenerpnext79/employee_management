import QRCode from 'qrcode'
import { getStoredWebCode } from './cookieHandler'

export const buildSpecificUrl = ({ pageName = '', targetCode = '', webCode = '' }) => {
  if (typeof window === 'undefined') return ''
  const origin = window.location.origin
  const currentPath = window.location.pathname.replace(/^\/|\/$/g, '')
  const hasHashRoute = window.location.hash.startsWith('#') || currentPath === '' || currentPath === 'frontend'

  const effectiveWebCode = webCode || (pageName ? getStoredWebCode(pageName) : '') || getStoredWebCode() || ''
  const params = new URLSearchParams()
  if (effectiveWebCode) {
    params.set('web_code', String(effectiveWebCode).split('#')[0].trim())
  }

  try {
    const searchParams = new URLSearchParams(window.location.search)
    searchParams.forEach((v, k) => {
      if (k !== 'web_code' && !params.has(k)) {
        params.set(k, v)
      }
    })
    const hash = window.location.hash || ''
    if (hash.includes('?')) {
      const hashQuery = hash.slice(hash.indexOf('?') + 1).split('#')[0]
      const hashParams = new URLSearchParams(hashQuery)
      hashParams.forEach((v, k) => {
        if (k !== 'web_code' && !params.has(k)) {
          params.set(k, v)
        }
      })
    }
  } catch (e) {}

  const queryString = params.toString() ? `?${params.toString()}` : ''
  const cleanPage = pageName || 'hr_employee_portal'
  const cleanTarget = targetCode ? String(targetCode).trim() : ''

  if (hasHashRoute) {
    if (cleanTarget) {
      return `${origin}/#${cleanPage}#${cleanTarget}${queryString}`
    }
    return `${origin}/#${cleanPage}${queryString}`
  }

  const base = currentPath ? `${origin}/${currentPath}` : `${origin}/${cleanPage}`
  if (cleanTarget) {
    return `${base}${queryString}#${cleanTarget}`
  }
  return `${base}${queryString}`
}

export const generateAndDownloadQrCode = async ({
  url,
  groupName = '',
  tabName = '',
  portalTitle = '',
  employeeName = ''
}) => {
  if (typeof window === 'undefined' || !url) return false

  try {
    const qrDataUrl = await QRCode.toDataURL(url, {
      width: 500,
      margin: 1,
      errorCorrectionLevel: 'M',
      color: {
        dark: '#000000',
        light: '#ffffff'
      }
    })

    const qrImage = new Image()
    await new Promise((resolve, reject) => {
      qrImage.onload = resolve
      qrImage.onerror = reject
      qrImage.src = qrDataUrl
    })

    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    const width = 560

    const cleanGroupName = (groupName && groupName !== 'Default Group') ? String(groupName).trim() : ''
    const cleanTabName = (tabName && tabName !== cleanGroupName) ? String(tabName).trim() : ''

    let contentExtraHeight = 0
    if (cleanGroupName && cleanTabName) {
      contentExtraHeight = 90
    } else if (cleanGroupName || cleanTabName) {
      contentExtraHeight = 55
    } else {
      contentExtraHeight = 20
    }

    const qrSize = 460
    const qrX = (width - qrSize) / 2
    const qrY = 32
    const height = qrY + qrSize + 25 + contentExtraHeight

    canvas.width = width
    canvas.height = height

    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, width, height)

    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 3
    ctx.strokeRect(8, 8, width - 16, height - 16)

    ctx.drawImage(qrImage, qrX, qrY, qrSize, qrSize)

    if (cleanGroupName || cleanTabName) {
      const lineY = qrY + qrSize + 14
      ctx.strokeStyle = '#e2e8f0'
      ctx.lineWidth = 1.5
      ctx.beginPath()
      ctx.moveTo(30, lineY)
      ctx.lineTo(width - 30, lineY)
      ctx.stroke()

      let currentY = lineY + 34

      if (cleanGroupName) {
        ctx.fillStyle = '#000000'
        ctx.font = 'bold 24px "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        const displayGroup = cleanGroupName.length > 36 ? cleanGroupName.substring(0, 34) + '...' : cleanGroupName
        ctx.fillText(displayGroup, width / 2, currentY)
        currentY += 34
      }

      if (cleanTabName) {
        ctx.fillStyle = '#000000'
        ctx.font = 'bold 20px "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        const displayTab = cleanTabName.length > 40 ? cleanTabName.substring(0, 38) + '...' : cleanTabName
        ctx.fillText(displayTab, width / 2, currentY)
      }
    }

    const cleanFileName = (cleanTabName || cleanGroupName || portalTitle || 'qr_code')
      .replace(/[^a-zA-Z0-9_-]/g, '_')
      .replace(/_+/g, '_')
      .slice(0, 50)

    const downloadLink = document.createElement('a')
    downloadLink.download = `${cleanFileName}_QR.png`
    downloadLink.href = canvas.toDataURL('image/png')
    document.body.appendChild(downloadLink)
    downloadLink.click()
    document.body.removeChild(downloadLink)

    return true
  } catch (error) {
    console.error('Failed to generate QR code', error)
    return false
  }
}

