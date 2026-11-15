import React from 'react'
import { createRoot } from 'react-dom/client'
import { createAgent } from '@ui-sdk/react/agent'
import { App } from './App'
import './styles.css'

export const diagnosticsAgent = createAgent({ allow: step => !step.confirm })
declare global { interface Window { diagnosticsAgent: typeof diagnosticsAgent } }
window.diagnosticsAgent = diagnosticsAgent
createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>)
