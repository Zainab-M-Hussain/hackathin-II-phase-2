"use client"

interface Task {
    id: number;
    title: string;
    description: string | null;
    completed: boolean;
}

interface TaskCardProps {
    task: Task;
}

export default function TaskCard({ task }: TaskCardProps) {
    return (
        <div className="p-4 border rounded mb-4">
            <h3 className="text-xl font-bold">{task.title}</h3>
            <p>{task.description}</p>
            <p>Completed: {task.completed ? "Yes" : "No"}</p>
        </div>
    )
}
