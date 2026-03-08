import { BASE_URL } from "./auth";

export async function getServices() {
    const response = await fetch(`${BASE_URL}/appointment/services`)
    if (!response.ok) return []
    return response.json()
}

export async function getAvailableSlots(token: string, serviceId: number, date: string) {
    const response = await fetch(
        `${BASE_URL}/appointment/available-slots?service_id=${serviceId}&date=${date}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )
    if (!response.ok) return []
    return response.json()
}

export async function createAppointment(token: string, data: object) {
    const response = await fetch(`${BASE_URL}/appointment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail)
    }
    return response.json()
}

export async function getAppointments(token: string) {
    const response = await fetch(`${BASE_URL}/appointment/`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` }
    })
    if (!response.ok) return []
    const data = await response.json()
    return data.appointments
}

export async function cancelAppointment(token: string, id: number) {
    const response = await fetch(`${BASE_URL}/appointment/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ status: 'cancelled' })
    })
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail)
    }
    return response.json()
}

export async function updateAppointment(token: string, id: number, data: object) {
    const response = await fetch(`${BASE_URL}/appointment/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail)
    }
    return response.json()
}