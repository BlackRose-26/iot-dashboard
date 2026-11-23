import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import * as Tooltip from '@radix-ui/react-tooltip'
import { AppProvider } from './state/AppContext'
import App from './App'
import '@fontsource-variable/open-sans'
import '@fontsource-variable/open-sans/wght-italic.css'
import '@fortawesome/fontawesome-free/css/fontawesome.min.css'
import '@fortawesome/fontawesome-free/css/solid.min.css'
import './styles/tailwind.css'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Tooltip.Provider delayDuration={250}>
        <AppProvider>
          <App />
        </AppProvider>
      </Tooltip.Provider>
    </BrowserRouter>
  </React.StrictMode>,
)
