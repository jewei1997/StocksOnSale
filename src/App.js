import React from 'react';
import './App.css';
import { Table } from 'react-bootstrap';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      // data = [{"ticker": t1, "pe_ratio": pe1, "market_cap": mc1},
      //         {"ticker": t2, "pe_ratio": pe2, "market_cap": mc2}, ...]
      data: [],
      is_ascending: true,
    }
  }

  // TODO: move this to a helpers file
  // Convert an array structured like [{"ticker": t1, "key": val1}, {"ticker": t2, "key": val2}, ...]
  // to a dict like: {t1: val1, t2: val2, ...}
  arrayToDict(arr, key) {
    let tickerToVal = {}
    for (let i = 0; i < arr.length; i++) {
      const stock = arr[i]
      tickerToVal[stock["ticker"]] = stock[key]
    }
    return tickerToVal
  }

  async componentDidMount() {
    const pe_resp = await fetch(`/stocks/pe_ratios/`)
    const pe_json = await pe_resp.json()
    const mc_resp = await fetch(`stocks/market_caps/`)
    const mc_json = await mc_resp.json()

    const tickerToPe = this.arrayToDict(pe_json.data, "pe_ratio")
    const tickerToMarketCap = this.arrayToDict(mc_json.data, "market_cap")

    // build data that looks like:
    // data = [{"ticker": t1, "pe_ratio": pe1, "market_cap": mc1},
    //         {"ticker": t2, "pe_ratio": pe2, "market_cap": mc2}, ...]
    let data = []
    for (const ticker in tickerToPe) {
      let pe_ratio = tickerToPe[ticker]
      let market_cap = tickerToMarketCap[ticker]
      let data_element = {"ticker": ticker, "pe_ratio": pe_ratio, "market_cap": market_cap}
      data.push(data_element)
    }

    // set data to this.state.data
    this.setState({data: data})
  }

  onSort(event, sortKey) {
    const data = this.state.data
    data.sort((a,b) => {
      let result
      if (typeof(a[sortKey]) === "number") {
        result = a[sortKey] - b[sortKey]
      } else {
        result = a[sortKey].localeCompare(b[sortKey])
      }
      if (this.state.is_ascending) { return result }
      return -result
    })
    this.state.is_ascending = !this.state.is_ascending
    this.setState({data: data})
  }

  numFormatter(num) {
    if (num < 999) {
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

  render() {
    const len = (this.state.data === undefined ? 0 : this.state.data.length)
    return (
        <Table striped bordered hover variant="dark">
          <thead>
          <tr>
            <th>Ticker</th>
            <th onClick={e => this.onSort(e, "pe_ratio")}>PE Ratio</th>
            <th onClick={e => this.onSort(e, "market_cap")}>Market Cap</th>
          </tr>
          </thead>
          <tbody>
          {Array.from({length: len}).map((_, index) => {
            const stock_data_ele = this.state.data[index]
            const ticker = stock_data_ele["ticker"]
            const pe_ratio = stock_data_ele["pe_ratio"]
            const market_cap = this.numFormatter(stock_data_ele["market_cap"])
            return (
                <tr>
                  <td key={index}><a href={'https://finance.yahoo.com/quote/' + ticker}>{ticker}</a></td>
                  <td key={len + index}>{pe_ratio}</td>
                  <td key={2*len + index}>{market_cap}</td>
                </tr>
            )
          })}
          </tbody>
        </Table>
    )
  }
}

export default App;
