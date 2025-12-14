"use client"

import { useState } from "react"
import { createUser } from "../services/api"

export default function RegisterForm() {
    const [email, setEmail] = useState("")
    const [name, setName] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        await createUser(email, name)
        setEmail("")
        setName("")
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                required
                className="p-2 border rounded"
            />
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Name"
                required
                className="p-2 border rounded"
            />
            <button type="submit" className="p-2 bg-blue-500 text-white rounded">Register</button>
        </form>
    )
}
