import React from 'react';
import './App.css';
import { Table } from 'react-bootstrap';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      data: [],
      is_ascending: true,
    }
  }

  async componentDidMount() {
    const response = await fetch(`/stocks/pe_ratios/`);
    const json = await response.json();
    this.setState({data: json["data"], is_ascending: true})
  }

  onSort(event, sortKey) {
    const data = this.state.data
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
    const len = (this.state.data === undefined ? 0 : this.state.data.length)
    return (
        <Table striped bordered hover variant="dark">
          <thead>
          <tr>
            <th>Ticker</th>
            <th onClick={e => this.onSort(e, "pe_ratio")}>PE Ratio</th>
          </tr>
          </thead>
          <tbody>
          {Array.from({length: len}).map((_, index) => {
            const ticker = this.state.data[index]["ticker"];
            const pe_ratio = this.state.data[index]["pe_ratio"];
            return (
                <tr>
                  <td key={index}><a href={'https://finance.yahoo.com/quote/' + ticker}>{ticker}</a></td>
                  <td key={len + index}>{pe_ratio}</td>
                </tr>
            )
          })}
          </tbody>
        </Table>
    )
  }
}

export default App;
