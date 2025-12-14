"use client"

import { useState, useEffect } from "react"
import TaskList from "./components/TaskList"
import TaskForm from "./components/TaskForm"
import { getTasks } from "./services/api"

export default function Home() {
    const [tasks, setTasks] = useState([])

    useEffect(() => {
        const fetchTasks = async () => {
            // Hardcoded user_id for now
            const tasks = await getTasks(1)
            setTasks(tasks)
        }
        fetchTasks()
    }, [])

    return (
        <main>
            <h1>Todo App</h1>
            <TaskForm />
            <TaskList tasks={tasks} />
        </main>
    )
}
