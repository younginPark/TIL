import React, {Component} from 'react';

class ToDoInfo extends Component {
    static defaultProps = {
        info: {
            id: 0,
            name: 'Name',
            due: '2000.00.00'
        }
    }

    state = {
        name: '',
        due: ''
    }

    handleRemove = () => {
        const{info, onRemove} = this.props;
        onRemove(info.id);
    }

    render() {
        const {name, due} = this.props.info;
        const style = {
            border: '1px solid black',
            padding: '8px',
        };
        return (
        <div style={style}>
            <div>
                <input type='checkbox'></input>
                {name} {due} <button onClick={this.handleRemove}>삭제</button>
            </div>
        </div>
        );
    }
}

export default ToDoInfo;
