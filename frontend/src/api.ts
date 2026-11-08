export type HealthResponse = {
  status: 'ok'
  service: string
}

export async function fetchHealth(signal: AbortSignal): Promise<HealthResponse> {
  const response = await fetch('/api/v1/health', { signal })

  if (!response.ok) {
    throw new Error(`Le service a répondu avec le code HTTP ${response.status}.`)
  }

  // TypeScript ne vérifie pas le JSON reçu sur le réseau : on le contrôle ici.
  const data: unknown = await response.json()

  if (
    typeof data !== 'object' ||
    data === null ||
    !('status' in data) ||
    data.status !== 'ok' ||
    !('service' in data) ||
    typeof data.service !== 'string'
  ) {
    throw new Error('La réponse du service est inattendue.')
  }

  return { status: data.status, service: data.service }
}
