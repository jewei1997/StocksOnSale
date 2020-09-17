// Convert an array structured like [{"ticker": t1, "key": val1}, {"ticker": t2, "key": val2}, ...]
// to a dict like: {t1: val1, t2: val2, ...}
export function arrayToDict(arr, key) {
  let tickerToVal = {}
  for (let i = 0; i < arr.length; i++) {
    const stock = arr[i]
    tickerToVal[stock["ticker"]] = stock[key]
  }
  return tickerToVal
}

export function numFormatter(num) {
  if (num === undefined) {
    return "N/A"
  } else if (num < 999) {
    return num
  } else if (999 < num && num < Math.pow(10,6)) {
    return (num/1000).toFixed(2) + 'K'; // convert to K for number from > 1000
  } else if (Math.pow(10, 6) <= num && num < Math.pow(10, 9)) {
    return (num/Math.pow(10, 6)).toFixed(2) + 'M'; // convert to M for number from > 1 million
  } else if (Math.pow(10, 9) <= num && num < Math.pow(10, 12)) {
    return (num/Math.pow(10, 9)).toFixed(2) + 'B'; // convert to B for number from > 1 billion
  } else if (Math.pow(10, 12) <= num && num < Math.pow(10, 15)) {
    return (num/Math.pow(10, 12)).toFixed(2) + 'T'; // convert to T for number from > 1 trillion
  }
}

export function percentFormatter(num) {
  if (num === undefined) {
    return "N/A"
  }
  return (num * 100).toFixed(2) + '%'
}

export function onSort(event, sortKey, data, is_ascending) {
  data.sort((a,b) => {
    let result
    if (a[sortKey] === undefined) {
      result = -1 // put b[sortKey] first
    } else if (b[sortKey] === undefined) {
      result = 1 // put a[sortKey] first
    } else if (typeof(a[sortKey]) === "number" && typeof(b[sortKey]) === "number") {
      result = a[sortKey] - b[sortKey]
    } else {
      result = a[sortKey].localeCompare(b[sortKey])
    }
    if (is_ascending) { return result }
    return -result
  })
  return data
}

