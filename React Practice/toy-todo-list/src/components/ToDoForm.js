import React, {Component} from 'react';

class ToDoForm extends Component{

  state = {
      name : '',
      due : ''
  }

  handleChange = (e) => {
    this.setState({
        [e.target.name]: e.target.value
    });
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.props.onCreate(this.state);
    this.setState({
        name: '',
        due: ''
    });
  }

  render(){
    return(
    <form onSubmit = {this.handleSubmit}>
        <input
            placeholder = "To Do thing"
            value = {this.state.name}
            onChange = {this.handleChange}
            name = "name"
        />
        <input
            placeholder = "Due Date"
            value = {this.state.due}
            onChange = { this.handleChange}
            name = "due"
        />
        <button type = "submit">등록</button>
    </form>
    );
  }
}

export default ToDoForm;
