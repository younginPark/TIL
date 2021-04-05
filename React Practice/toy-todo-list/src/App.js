import React, {Component} from 'react';
import ToDoForm from './components/ToDoForm'
import ToDoInfoList from './components/ToDoInfoList'

class App extends Component{
  id = 1
  state = {
    todo_list : [
      {id : 0,
      name : '밥 먹기',
      due: '2021.05.05'}
    ],
  }

  handleCreate = (data) => {
    const {todo_list} = this.state;
    this.setState({
      todo_list: todo_list.concat({id: this.id++, ...data})
    });
    console.log({todo_list});
  }

  handleRemove = (id) => {
    const {todo_list} = this.state;
    this.setState({
      todo_list: todo_list.filter(info => info.id != id)
    });
  }

  render(){
    const {todo_list} = this.state;
    const style = {
      margin: '8px',
      padding: '8px'
    }
    return(
      <div style={style}>
        <div><b>To Do List</b></div>
        <ToDoForm onCreate = {this.handleCreate}/>
        {/* <div>{JSON.stringify(todo_list)}</div> */}
        <ToDoInfoList 
          data = {todo_list}
          onRemove = {this.handleRemove}
        />
      </div>
    );
  }
}

export default App;
