import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      results: []
    };
    this.handleBackground = this.handleBackground.bind(this);
  }

  handleBackground(event) {
    var reader = new FileReader();
    const seft = this;
    reader.onloadend = function () {
      const formData = new FormData();
      formData.append("fileBase64", reader.result);
      axios
        .post("http://localhost:5000/predict", formData)
        .then((res) => {
          console.log(res);
          if (res.status === 200) {
            seft.setState({ results: res.data.predicted });
          }
        })
        .catch((err) => {
          seft.setState({ results: ["Not result"] });
        });
    };
    reader.readAsDataURL(event.target.files[0]);
  }

  render() {
    return (
      <div>
        <div>Result : </div>
        <ul>
          {this.state.results.map((item) => {
            return <li>{item}</li>;
          })}
        </ul>
        <input
          accept="image/*"
          onChange={this.handleBackground}
          id="text-button-file"
          type="file"
        />
      </div>
    );
  }
}

export default App;
