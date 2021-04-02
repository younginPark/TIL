import React, { Component } from 'react';

class PhoneForm extends Component{
    state = {
        name: '',
        phone: ''
    }
    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
    }
    handleSubmit = (e) => {
        e.preventDefault(); //페이지 리로딩 방지
        this.props.onCreate(this.state); //상대값을 onCreate를 통해 부모에게 전달
        this.setState({
            name: '',
            phone: ''
        })
    }
    render(){
        return (
            <form onSubmit = {this.handleSubmit}>
                <input
                    placeholder = "Name"
                    value = {this.state.name}
                    onChange = {this.handleChange}
                    name = "name"
                />
                <input
                    placeholder = "Phone Number"
                    value = {this.state.phone}
                    onChange = { this.handleChange}
                    name = "phone"
                />
                <button type = "submit">등록</button>
            </form>
        );
    }
}

export default PhoneForm;