export interface User {
    username: string;
    region: string;
    country: string;
}

export interface WeatherData {
    temperature: number;
    humidity: number;
    description: string;
    timestamp: string;
}

export interface Recommendation {
    should_irrigate: boolean;
    intensity: string;
    reason: string;
    temperature_status: string;
    humidity_status: string;
    warnings: string[];
}

export interface Notification {
    id?: string;
    type: string;
    message: string;
    severity: string;
    timestamp: string;
    details: string;
}

export interface ApiResponse<T> {
    data: T;
    message?: string;
    error?: string;
}