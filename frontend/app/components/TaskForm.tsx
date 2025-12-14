"use client"

import { useState } from "react"
import { createTask } from "../services/api"

export default function TaskForm() {
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        // Hardcoded user_id for now
        await createTask(1, title, description)
        setTitle("")
        setDescription("")
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 mb-4">
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Title"
                required
                className="p-2 border rounded"
            />
            <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Description"
                className="p-2 border rounded"
            />
            <button type="submit" className="p-2 bg-blue-500 text-white rounded">Add Task</button>
        </form>
    )
}
