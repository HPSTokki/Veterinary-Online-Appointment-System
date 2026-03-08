export const BASE_URL = import.meta.env.API_URL ?? 'http://localhost:8000' 
export const CHAIN_URL = `https://veterinary-online-appointment-syste.vercel.app/${BASE_URL}`

interface RegisterData {
    email: string
    password: string
}

interface LoginData {
    email: string
    password: string
}

export async function registerUser(form_data: RegisterData) {
    const response = await fetch(`${CHAIN_URL}/user/auth/reg`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: form_data.email,
            password_hash: form_data.password
        })
    })

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail) 
    }

    return response.json()

}

export async function loginUser(form_data: LoginData) {
    const formData = new URLSearchParams()
    formData.append('username', form_data.email)
    formData.append('password', form_data.password)

    const response = await fetch(`${BASE_URL}/user/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
    })

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail)
    }

    return response.json()

}

export async function getMe(token: string) {
    const response = await fetch(`${CHAIN_URL}/user/me`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })

    if (!response.ok) {
        throw new Error('Unauthorized')
    }

    return response.json()
}