const LOCALE = 'es-CO'
const EMPTY_VALUE = '—'
const PERCENTAGE_FACTOR = 100

const moneyFormatter = new Intl.NumberFormat(LOCALE, {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})
const indexFormatter = new Intl.NumberFormat(LOCALE, {
  minimumFractionDigits: 2,
  maximumFractionDigits: 4,
})
const percentageFormatter = new Intl.NumberFormat(LOCALE, { maximumFractionDigits: 2 })

function formatOrEmpty(value, format) {
  return value === null || value === undefined ? EMPTY_VALUE : format(value)
}

export function formatMoney(value) {
  return formatOrEmpty(value, (amount) => {
    const sign = amount < 0 ? '-' : ''
    return `${sign}$${moneyFormatter.format(Math.abs(amount))}`
  })
}

export function formatIndex(value) {
  return formatOrEmpty(value, (index) => indexFormatter.format(index))
}

export function formatPercentage(value) {
  return formatOrEmpty(value, (percentage) => `${percentageFormatter.format(percentage)}%`)
}

export function formatRatioAsPercentage(ratio) {
  return formatOrEmpty(ratio, (value) => formatPercentage(value * PERCENTAGE_FACTOR))
}
