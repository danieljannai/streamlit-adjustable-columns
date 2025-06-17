// Import Streamlit's component base
import { Streamlit } from "streamlit-component-lib"

/**
 * Creates resize handles that align with Streamlit columns below
 */
function onRender(event) {
    const data = event.detail
    const config = data.args.config
    const widths = config.widths
    const labels = config.labels || widths.map((_, i) => `Col ${i+1}`)
    const gap = config.gap || "small"
    const border = config.border || false
    
    // Minimum width constraint: 6% for all columns
    const MIN_WIDTH_RATIO = 0.06
    
    // Clear the container
    const container = document.getElementById("root")
    container.innerHTML = ""
    
    // Store current state
    let currentWidths = [...widths]
    let isResizing = false
    let startX = 0
    let startWidths = []
    let resizingIndex = -1
    
    // Get Streamlit theme colors
    const theme = {
        primary: getComputedStyle(document.documentElement).getPropertyValue('--primary-color') || '#ff6b6b',
        background: getComputedStyle(document.documentElement).getPropertyValue('--background-color') || '#ffffff',
        secondary: getComputedStyle(document.documentElement).getPropertyValue('--secondary-background-color') || '#f0f2f6',
        text: getComputedStyle(document.documentElement).getPropertyValue('--text-color') || '#262730',
        border: getComputedStyle(document.documentElement).getPropertyValue('--border-color') || '#e6eaf1'
    }
    
    // Define gap sizes (matching Streamlit's gap values)
    const gapSizes = {
        small: '0.5rem',
        medium: '1rem', 
        large: '1.5rem'
    }
    
    // Create the resize handle container that mimics the column layout
    const handleContainer = document.createElement("div")
    handleContainer.className = "resize-handle-container"
    handleContainer.style.cssText = `
        display: flex;
        width: 100%;
        height: 40px;
        gap: ${gapSizes[gap]};
        position: relative;
        box-sizing: border-box;
        background: transparent;
        margin-bottom: 10px;
        align-items: center;
    `
    
    // Calculate total width for proportions
    const totalWidth = currentWidths.reduce((sum, w) => sum + w, 0)
    
    // Create handle areas that match the column layout exactly
    const handleAreas = []
    currentWidths.forEach((width, index) => {
        const widthPercentage = (width / totalWidth) * 100
        
        // Create handle area that matches column width
        const handleArea = document.createElement("div")
        handleArea.className = "handle-area"
        handleArea.style.cssText = `
            flex: 0 0 ${widthPercentage}%;
            height: 100%;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            background: ${border ? 'rgba(230, 234, 241, 0.1)' : 'transparent'};
            ${border ? 'border: 1px dashed rgba(230, 234, 241, 0.3);' : ''}
            border-radius: 4px;
            box-sizing: border-box;
            transition: all 0.15s ease;
        `
        
        // Add column label
        const label = document.createElement("div")
        label.textContent = labels[index]
        label.style.cssText = `
            font-size: 11px;
            color: ${theme.text}60;
            font-weight: 500;
            opacity: 0.7;
            pointer-events: none;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 90%;
        `
        
        handleArea.appendChild(label)
        
        // Add hover effect for the handle area
        handleArea.addEventListener('mouseenter', () => {
            if (!isResizing) {
                handleArea.style.background = border ? 'rgba(230, 234, 241, 0.2)' : 'rgba(230, 234, 241, 0.1)'
                label.style.opacity = '1'
            }
        })
        
        handleArea.addEventListener('mouseleave', () => {
            if (!isResizing) {
                handleArea.style.background = border ? 'rgba(230, 234, 241, 0.1)' : 'transparent'
                label.style.opacity = '0.7'
            }
        })
        
        // Create resize handle (except for last area)
        if (index < currentWidths.length - 1) {
            const resizeHandle = document.createElement("div")
            resizeHandle.className = "resize-handle"
            resizeHandle.style.cssText = `
                position: absolute;
                right: calc(-${gapSizes[gap]} / 2 - 3px);
                top: 50%;
                transform: translateY(-50%);
                width: 6px;
                height: 80%;
                cursor: col-resize;
                z-index: 1001;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 3px;
                transition: all 0.15s ease;
                background: transparent;
            `
            
            // Visual indicator for the handle
            const handleBar = document.createElement("div")
            handleBar.className = "handle-bar"
            handleBar.style.cssText = `
                width: 2px;
                height: 70%;
                background: ${theme.text}40;
                border-radius: 1px;
                transition: all 0.15s ease;
            `
            
            resizeHandle.appendChild(handleBar)
            resizeHandle.dataset.index = index
            
            // Handle hover effects
            resizeHandle.addEventListener('mouseenter', () => {
                if (!isResizing) {
                    handleBar.style.background = theme.primary
                    handleBar.style.width = '4px'
                    resizeHandle.style.background = `${theme.primary}15`
                }
            })
            
            resizeHandle.addEventListener('mouseleave', () => {
                if (!isResizing) {
                    handleBar.style.background = `${theme.text}40`
                    handleBar.style.width = '2px'
                    resizeHandle.style.background = 'transparent'
                }
            })
            
            // Handle mouse events for resizing
            resizeHandle.addEventListener('mousedown', (e) => startResize(e, resizeHandle, handleBar))
            
            handleArea.appendChild(resizeHandle)
        }
        
        handleAreas.push(handleArea)
        handleContainer.appendChild(handleArea)
    })
    
    container.appendChild(handleContainer)
    
    function startResize(e, handle, handleBar) {
        isResizing = true
        startX = e.clientX
        resizingIndex = parseInt(handle.dataset.index)
        startWidths = [...currentWidths]
        
        // Visual feedback
        handleBar.style.background = theme.primary
        handleBar.style.width = '4px'
        handle.style.background = `${theme.primary}25`
        
        // Dim all labels during resize
        handleAreas.forEach(area => {
            const label = area.querySelector('div')
            if (label) {
                label.style.opacity = '0.3'
                area.style.background = 'rgba(230, 234, 241, 0.05)'
            }
        })
        
        document.addEventListener('mousemove', handleResize)
        document.addEventListener('mouseup', stopResize)
        
        // Prevent text selection during resize
        document.body.style.userSelect = 'none'
        document.body.style.cursor = 'col-resize'
        e.preventDefault()
    }
    
    function handleResize(e) {
        if (!isResizing) return
        
        const deltaX = e.clientX - startX
        const containerWidth = handleContainer.offsetWidth
        const totalCurrentWidth = currentWidths.reduce((sum, w) => sum + w, 0)
        
        // Calculate change in ratio based on container width
        const deltaRatio = (deltaX / containerWidth) * totalCurrentWidth
        
        const leftIndex = resizingIndex
        const rightIndex = resizingIndex + 1
        
        // Apply minimum constraints
        const leftMin = MIN_WIDTH_RATIO * totalCurrentWidth
        const rightMin = MIN_WIDTH_RATIO * totalCurrentWidth
        
        let newLeftWidth = Math.max(leftMin, startWidths[leftIndex] + deltaRatio)
        let newRightWidth = Math.max(rightMin, startWidths[rightIndex] - deltaRatio)
        
        // Handle constraint violations
        if (newLeftWidth < leftMin) {
            newLeftWidth = leftMin
            newRightWidth = startWidths[rightIndex] + (startWidths[leftIndex] - leftMin)
        }
        if (newRightWidth < rightMin) {
            newRightWidth = rightMin
            newLeftWidth = startWidths[leftIndex] + (startWidths[rightIndex] - rightMin)
        }
        
        currentWidths[leftIndex] = newLeftWidth
        currentWidths[rightIndex] = newRightWidth
        
        // Update handle area widths immediately
        updateHandleWidths()
    }
    
    function updateHandleWidths() {
        const newTotal = currentWidths.reduce((sum, w) => sum + w, 0)
        
        handleAreas.forEach((area, index) => {
            const widthPercentage = (currentWidths[index] / newTotal) * 100
            area.style.flex = `0 0 ${widthPercentage}%`
        })
    }
    
    function stopResize(e) {
        if (!isResizing) return
        
        isResizing = false
        document.removeEventListener('mousemove', handleResize)
        document.removeEventListener('mouseup', stopResize)
        
        // Reset body styles
        document.body.style.userSelect = ''
        document.body.style.cursor = ''
        
        // Reset all handle visuals
        const handles = handleContainer.querySelectorAll('.resize-handle')
        handles.forEach(handle => {
            const handleBar = handle.querySelector('.handle-bar')
            if (handleBar) {
                handleBar.style.background = `${theme.text}40`
                handleBar.style.width = '2px'
            }
            handle.style.background = 'transparent'
        })
        
        // Reset handle areas
        handleAreas.forEach(area => {
            const label = area.querySelector('div')
            if (label) {
                label.style.opacity = '0.7'
                area.style.background = border ? 'rgba(230, 234, 241, 0.1)' : 'transparent'
            }
        })
        
        // Send updated widths back to Streamlit
        Streamlit.setComponentValue({
            widths: currentWidths,
            action: "resize"
        })
    }
    
    // Set compact frame height
    Streamlit.setFrameHeight(60)
    
    // Add global styles for better integration
    const style = document.createElement('style')
    style.textContent = `
        .resize-handle-container {
            font-family: inherit;
        }
        
        .handle-area {
            min-width: 6% !important;
        }
        
        .resize-handle:hover .handle-bar {
            background: ${theme.primary} !important;
            width: 4px !important;
        }
        
        .resize-handle.resizing {
            background: ${theme.primary}25 !important;
        }
        
        .resize-handle.resizing .handle-bar {
            background: ${theme.primary} !important;
            width: 4px !important;
        }
        
        /* Smooth transitions for handle area width changes */
        .handle-area {
            transition: flex 0.1s ease-out;
        }
        
        /* Ensure clean appearance */
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        
        #root {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
    `
    document.head.appendChild(style)
}

// Attach our function to the onRender event
Streamlit.events.addEventListener("streamlit:render", onRender)

// Tell Streamlit we're ready to receive data
Streamlit.setComponentReady() 