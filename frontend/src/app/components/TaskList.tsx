"use client"

import TaskCard from "./TaskCard"
import { Task } from "../types/task";
import { motion, AnimatePresence } from "framer-motion";

interface TaskListProps {
    tasks: Task[];
    refreshTasks: () => void;
    selectedTaskIds: string[];
    onSelectedTasksChange: (selectedIds: string[]) => void;
}

export default function TaskList({ tasks, refreshTasks, selectedTaskIds, onSelectedTasksChange }: TaskListProps) {

    const handleSelectToggle = (taskId: string) => {
        const newSelected = selectedTaskIds.includes(taskId)
            ? selectedTaskIds.filter(id => id !== taskId)
            : [...selectedTaskIds, taskId];
        onSelectedTasksChange(newSelected);
    };

    const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.checked) {
            const allTaskIds = tasks && Array.isArray(tasks) ? tasks.map(task => task.id) : [];
            onSelectedTasksChange(allTaskIds);
        } else {
            onSelectedTasksChange([]);
        }
    };

    return (
        <div>
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-3 mb-6 p-4 bg-gray-800/30 backdrop-blur-sm rounded-xl border border-gray-700/50"
            >
                <input
                    type="checkbox"
                    checked={selectedTaskIds.length === tasks.length && tasks.length > 0}
                    onChange={handleSelectAll}
                    className="form-checkbox h-5 w-5 text-indigo-500 rounded focus:ring-indigo-500 border-gray-600 bg-gray-700"
                />
                <label className="text-sm text-gray-300">
                    Select All ({selectedTaskIds.length} selected)
                </label>
                <div className="ml-auto flex items-center gap-4">
                    <span className="text-sm text-gray-400">
                        {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                    </span>
                    {tasks.length > 0 && (
                        <span className="px-2 py-1 bg-indigo-500/20 text-indigo-400 rounded-full text-xs font-medium border border-indigo-500/30">
                            Active
                        </span>
                    )}
                </div>
            </motion.div>

            <AnimatePresence>
                {tasks && Array.isArray(tasks) && tasks.map(task => (
                    <motion.div
                        key={`motion-${task.id}`}
                        layout
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                    >
                        <TaskCard
                            key={`card-${task.id}`}
                            task={task}
                            refreshTasks={refreshTasks}
                            onSelectToggle={handleSelectToggle}
                            isSelected={selectedTaskIds.includes(task.id)}
                        />
                    </motion.div>
                ))}
            </AnimatePresence>

            {tasks.length === 0 && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center py-16 px-4"
                >
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-500/10 mb-6">
                        <span className="text-3xl">📋</span>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">No tasks yet</h3>
                    <p className="text-gray-400 mb-6 max-w-md mx-auto">Add your first task to start organizing your workflow</p>
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-gray-800/50 rounded-lg border border-gray-700">
                        <span className="text-sm text-gray-400">💡 Pro tip:</span>
                        <span className="text-sm text-gray-300">Break large projects into smaller, actionable tasks</span>
                    </div>
                </motion.div>
            )}
        </div>
    )
}