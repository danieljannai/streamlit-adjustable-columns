// Import Streamlit's component base
import { Streamlit } from "streamlit-component-lib"

/**
 * Creates resize handles positioned at exact column boundaries
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
    
    // Gap sizes that match Streamlit exactly (from CSS inspection)
    const gapSizes = {
        small: 8,   // 0.5rem = 8px
        medium: 16, // 1rem = 16px  
        large: 24   // 1.5rem = 24px
    }
    
    const gapPixels = gapSizes[gap]
    
    // Create main container
    const handleContainer = document.createElement("div")
    handleContainer.className = "resize-handle-container"
    handleContainer.style.cssText = `
        position: relative;
        width: 100%;
        height: 40px;
        background: transparent;
        margin-bottom: 8px;
    `
    
    // Calculate column positions based on widths and gaps
    function calculateColumnPositions(containerWidth) {
        const totalWidth = currentWidths.reduce((sum, w) => sum + w, 0)
        const totalGapWidth = (currentWidths.length - 1) * gapPixels
        const availableWidth = containerWidth - totalGapWidth
        
        let positions = []
        let currentPos = 0
        
        for (let i = 0; i < currentWidths.length; i++) {
            const columnWidth = (currentWidths[i] / totalWidth) * availableWidth
            positions.push({
                start: currentPos,
                width: columnWidth,
                end: currentPos + columnWidth
            })
            currentPos += columnWidth + gapPixels
        }
        
        return positions
    }
    
    // Create column indicators and resize handles
    function updateLayout() {
        handleContainer.innerHTML = ""
        const containerWidth = handleContainer.offsetWidth || 800 // fallback
        const positions = calculateColumnPositions(containerWidth)
        
        positions.forEach((pos, index) => {
            // Create column indicator
            const indicator = document.createElement("div")
            indicator.className = "column-indicator"
            indicator.style.cssText = `
                position: absolute;
                left: ${pos.start}px;
                width: ${pos.width}px;
                height: 100%;
                background: ${border ? 'rgba(230, 234, 241, 0.1)' : 'rgba(100, 100, 100, 0.05)'};
                ${border ? 'border: 1px dashed rgba(230, 234, 241, 0.3);' : ''}
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.15s ease;
                box-sizing: border-box;
            `
            
            // Add label
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
            
            indicator.appendChild(label)
            
            // Hover effect
            indicator.addEventListener('mouseenter', () => {
                if (!isResizing) {
                    indicator.style.background = border ? 'rgba(230, 234, 241, 0.2)' : 'rgba(100, 100, 100, 0.1)'
                    label.style.opacity = '1'
                }
            })
            
            indicator.addEventListener('mouseleave', () => {
                if (!isResizing) {
                    indicator.style.background = border ? 'rgba(230, 234, 241, 0.1)' : 'rgba(100, 100, 100, 0.05)'
                    label.style.opacity = '0.7'
                }
            })
            
            handleContainer.appendChild(indicator)
            
            // Create resize handle at the boundary (except for last column)
            if (index < positions.length - 1) {
                const handle = document.createElement("div")
                handle.className = "resize-handle"
                handle.style.cssText = `
                    position: absolute;
                    left: ${pos.end + gapPixels / 2 - 4}px;
                    top: 0;
                    width: 8px;
                    height: 100%;
                    cursor: col-resize;
                    z-index: 1001;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 4px;
                    transition: all 0.15s ease;
                    background: transparent;
                `
                
                // Visual handle bar
                const handleBar = document.createElement("div")
                handleBar.style.cssText = `
                    width: 2px;
                    height: 70%;
                    background: ${theme.text}40;
                    border-radius: 1px;
                    transition: all 0.15s ease;
                `
                
                handle.appendChild(handleBar)
                handle.dataset.index = index
                
                // Handle events
                handle.addEventListener('mouseenter', () => {
                    if (!isResizing) {
                        handleBar.style.background = theme.primary
                        handleBar.style.width = '4px'
                        handle.style.background = `${theme.primary}15`
                    }
                })
                
                handle.addEventListener('mouseleave', () => {
                    if (!isResizing) {
                        handleBar.style.background = `${theme.text}40`
                        handleBar.style.width = '2px'
                        handle.style.background = 'transparent'
                    }
                })
                
                handle.addEventListener('mousedown', (e) => startResize(e, handle, handleBar))
                
                handleContainer.appendChild(handle)
            }
        })
    }
    
    function startResize(e, handle, handleBar) {
        isResizing = true
        startX = e.clientX
        resizingIndex = parseInt(handle.dataset.index)
        startWidths = [...currentWidths]
        
        // Visual feedback
        handleBar.style.background = theme.primary
        handleBar.style.width = '4px'
        handle.style.background = `${theme.primary}25`
        
        // Dim indicators
        const indicators = handleContainer.querySelectorAll('.column-indicator')
        indicators.forEach(indicator => {
            indicator.style.background = 'rgba(100, 100, 100, 0.03)'
            const label = indicator.querySelector('div')
            if (label) label.style.opacity = '0.3'
        })
        
        document.addEventListener('mousemove', handleResize)
        document.addEventListener('mouseup', stopResize)
        
        // Prevent text selection
        document.body.style.userSelect = 'none'
        document.body.style.cursor = 'col-resize'
        e.preventDefault()
    }
    
    function handleResize(e) {
        if (!isResizing) return
        
        const deltaX = e.clientX - startX
        const containerWidth = handleContainer.offsetWidth
        const totalGapWidth = (currentWidths.length - 1) * gapPixels
        const availableWidth = containerWidth - totalGapWidth
        const totalCurrentWidth = currentWidths.reduce((sum, w) => sum + w, 0)
        
        // Calculate change in ratio
        const deltaRatio = (deltaX / availableWidth) * totalCurrentWidth
        
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
        
        // Update layout immediately
        updateLayout()
    }
    
    function stopResize(e) {
        if (!isResizing) return
        
        isResizing = false
        document.removeEventListener('mousemove', handleResize)
        document.removeEventListener('mouseup', stopResize)
        
        // Reset styles
        document.body.style.userSelect = ''
        document.body.style.cursor = ''
        
        // Reset handle visuals
        const handles = handleContainer.querySelectorAll('.resize-handle')
        handles.forEach(handle => {
            const handleBar = handle.querySelector('div')
            if (handleBar) {
                handleBar.style.background = `${theme.text}40`
                handleBar.style.width = '2px'
            }
            handle.style.background = 'transparent'
        })
        
        // Reset indicators
        const indicators = handleContainer.querySelectorAll('.column-indicator')
        indicators.forEach(indicator => {
            indicator.style.background = border ? 'rgba(230, 234, 241, 0.1)' : 'rgba(100, 100, 100, 0.05)'
            const label = indicator.querySelector('div')
            if (label) label.style.opacity = '0.7'
        })
        
        // Send updated widths back to Streamlit
        Streamlit.setComponentValue({
            widths: currentWidths,
            action: "resize"
        })
    }
    
    container.appendChild(handleContainer)
    
    // Initial layout
    updateLayout()
    
    // Update layout on resize
    const resizeObserver = new ResizeObserver(() => {
        updateLayout()
    })
    resizeObserver.observe(handleContainer)
    
    // Set frame height
    Streamlit.setFrameHeight(60)
    
    // Add styles
    const style = document.createElement('style')
    style.textContent = `
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
        
        .resize-handle:hover {
            background-color: ${theme.primary}15 !important;
        }
        
        .column-indicator {
            transition: background 0.15s ease, opacity 0.15s ease;
        }
        
        .resize-handle {
            transition: background 0.15s ease;
        }
    `
    document.head.appendChild(style)
}

// Attach our function to the onRender event
Streamlit.events.addEventListener("streamlit:render", onRender)

// Tell Streamlit we're ready to receive data
Streamlit.setComponentReady() 