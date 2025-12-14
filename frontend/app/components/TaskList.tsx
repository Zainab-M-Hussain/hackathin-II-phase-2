"use client"

import TaskCard from "./TaskCard"

interface Task {
    id: number;
    title: string;
    description: string | null;
    completed: boolean;
}

interface TaskListProps {
    tasks: Task[];
}

export default function TaskList({ tasks }: TaskListProps) {
    return (
        <div>
            {tasks.map(task => (
                <TaskCard key={task.id} task={task} />
            ))}
        </div>
    )
}
