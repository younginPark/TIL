import React, {Component} from 'react';
import ToDoInfo from './ToDoInfo'
class ToDoInfoList extends Component{

  static defaultProps = {
    data: [],
    onRemove: () => console.warn('onRemove not defined')
  }

  render(){
    const{ data, onRemove} = this.props;
    const list = data.map(
      info => (
        <ToDoInfo
          key = {info.id}
          info = {info}
          onRemove = {onRemove}
        />
      )
    );
    return(
        <div>{list}</div>
    );
  }
}

export default ToDoInfoList;
