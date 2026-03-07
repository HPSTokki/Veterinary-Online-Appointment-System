import { BASE_URL } from "./auth";

export interface CreatePetData {
    name: string
    breed: string
    species_type: string
    is_spayed_neutered: boolean
    sex: string
    date_of_birth: string
    weight_kg: number | null
}

export async function getPets(token: string) {
    const response = await fetch(`${BASE_URL}/pet/`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    if (!response.ok) return []
    const data = await response.json()
    return data.pets
}

export async function createPet(token: string, data: CreatePetData) {
    const response = await fetch(`${BASE_URL}/pet/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail)
    }
    return response.json()
}

export async function updatePet(token: string, petId: number, data: object) {
    const response = await fetch(`${BASE_URL}/pet/${petId}`, {
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