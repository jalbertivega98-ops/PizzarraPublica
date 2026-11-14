import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'
import Portrait from './Portrait'

const portrait = new URLSearchParams(location.search).get('portrait') === '1'
createRoot(document.getElementById('root')!).render(portrait ? <Portrait /> : <App />)
