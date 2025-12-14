const API_URL = "http://localhost:8000/api";

export const createUser = async (email: string, name: string) => {
    const response = await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, name }),
    });
    return response.json();
};

export const getTasks = async (userId: number) => {
    const response = await fetch(`${API_URL}/${userId}/tasks/`);
    return response.json();
};

export const createTask = async (userId: number, title: string, description: string) => {
    const response = await fetch(`${API_URL}/${userId}/tasks/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description }),
    });
    return response.json();
};

export const updateTask = async (userId: number, taskId: number, title: string, description: string, completed: boolean) => {
    const response = await fetch(`${API_URL}/${userId}/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description, completed }),
    });
    return response.json();
};

export const deleteTask = async (userId: number, taskId: number) => {
    const response = await fetch(`${API_URL}/${userId}/tasks/${taskId}`, {
        method: "DELETE",
    });
    return response.json();
};
