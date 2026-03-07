import { BASE_URL } from "./auth";

export interface CreateProfileData {
    full_name: string
    mobile_no: string | null
    tel_no: string | null
    preferred_contact_method: string 
    address: string
}

export interface UpdateProfileData {
    mobile_no?: string | null
    tel_no?: string | null
    preferred_contact_method?: string
    address?: string
}

export async function getClientProfile(token: string) {
    const response = await fetch(`${BASE_URL}/client/profile/me`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    if (!response.ok) return null
    return response.json()
}

export async function createClientProfile(token: string, data: CreateProfileData) {
    const response = await fetch(`${BASE_URL}/client/profile`, {
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

export async function updateProfile(token: string, data: UpdateProfileData) {
    const response = await fetch(`${BASE_URL}/client/profile/me`, {
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

