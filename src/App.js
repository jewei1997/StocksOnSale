import React from 'react';
import './App.css';
import { Table } from 'react-bootstrap';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      pe_ratios: [],
      market_caps: [],
      is_ascending: true,
    }
  }

  async componentDidMount() {
    const pe_resp = await fetch(`/stocks/pe_ratios/`)
    const pe_json = await pe_resp.json()
    this.setState({pe_ratios: pe_json["data"]})
    const mc_resp = await fetch(`stocks/market_caps/`)
    const mc_json = await mc_resp.json()
    this.setState({market_caps: mc_json["data"]})
  }

  onSort(event, sortKey) {
    const data = this.state.pe_ratios
    data.sort((a,b) => {
      let result = -1;
      if (typeof(a[sortKey]) === "number") {
        result = a[sortKey] - b[sortKey]
      } else {
        result = a[sortKey].localeCompare(b[sortKey])
      }
      if (this.state.is_ascending) {
        return result
      } else {
        return -1 * result
      }
    })
    this.state.is_ascending = !this.state.is_ascending
    this.setState({data: data})
  }

  render() {
    const len = (this.state.pe_ratios === undefined ? 0 : this.state.pe_ratios.length)
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
            const ticker = this.state.pe_ratios[index]["ticker"];
            const pe_ratio = this.state.pe_ratios[index] === undefined ? "unavailable" : this.state.pe_ratios[index]["pe_ratio"];
            const market_cap = this.state.market_caps[index] === undefined ? "unavailable" : this.state.market_caps[index]["market_cap"]
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
