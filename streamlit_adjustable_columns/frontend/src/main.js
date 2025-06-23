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
    const hidden = config.hidden || widths.map(() => false)
    
    // Minimum width constraint: 6% for all columns
    const MIN_WIDTH_RATIO = 0.06
    
    // Clear the container
    const container = document.getElementById("root")
    container.innerHTML = ""
    
    // Store current state
    let currentWidths = [...widths]
    let currentHidden = [...hidden]
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
        
        // Create a single, shared tooltip that is not constrained by column width
        const tooltip = document.createElement("div")
        tooltip.textContent = "Double-click to hide/show column"
        tooltip.style.cssText = `
            position: absolute;
            top: -2px; /* Position it in the margin space above the indicators */
            left: 0; /* Will be updated on hover */
            transform: translateX(-50%);
            background: ${theme.text};
            color: ${theme.background};
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 11px;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease, transform 0.1s ease;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            font-weight: 500;
        `
        handleContainer.appendChild(tooltip)
        
        positions.forEach((pos, index) => {
            // Create column indicator
            const indicator = document.createElement("div")
            indicator.className = "column-indicator"
            indicator.style.cssText = `
                position: absolute;
                left: ${pos.start}px;
                width: ${pos.width}px;
                height: 100%;
                background: ${currentHidden[index] ? 'rgba(255, 107, 107, 0.1)' : (border ? 'rgba(230, 234, 241, 0.1)' : 'rgba(100, 100, 100, 0.05)')};
                ${border ? 'border: 1px dashed rgba(230, 234, 241, 0.3);' : ''}
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.15s ease;
                box-sizing: border-box;
                cursor: pointer;
                user-select: none;
            `
            
            // Add label
            const label = document.createElement("div")
            label.textContent = labels[index]
            label.style.cssText = `
                font-size: 11px;
                color: ${currentHidden[index] ? theme.primary : theme.text + '60'};
                font-weight: 500;
                opacity: ${currentHidden[index] ? '0.8' : '0.7'};
                pointer-events: none;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 90%;
            `
            
            indicator.appendChild(label)
            
            // Add hidden indicator
            if (currentHidden[index]) {
                const hiddenIcon = document.createElement("div")
                hiddenIcon.innerHTML = "👁️"
                hiddenIcon.style.cssText = `
                    position: absolute;
                    top: 2px;
                    right: 4px;
                    font-size: 10px;
                    opacity: 0.7;
                    pointer-events: none;
                `
                indicator.appendChild(hiddenIcon)
            }
            
            // Show tooltip on hover
            indicator.addEventListener('mouseenter', () => {
                if (!isResizing) {
                    indicator.style.background = currentHidden[index] ? 
                        'rgba(255, 107, 107, 0.2)' : 
                        (border ? 'rgba(230, 234, 241, 0.2)' : 'rgba(100, 100, 100, 0.1)')
                    label.style.opacity = '1'
                    
                    // Position and show the shared tooltip, ensuring it's not clipped
                    const containerWidth = handleContainer.offsetWidth;
                    const tooltipWidth = tooltip.offsetWidth;
                    let targetLeft = pos.start + pos.width / 2;

                    // Adjust position to prevent clipping at the component edges
                    if (targetLeft - tooltipWidth / 2 < 0) {
                        // Nudge right if clipped on the left
                        targetLeft = tooltipWidth / 2;
                    } else if (targetLeft + tooltipWidth / 2 > containerWidth) {
                        // Nudge left if clipped on the right
                        targetLeft = containerWidth - tooltipWidth / 2;
                    }
                    
                    tooltip.style.left = `${targetLeft}px`;
                    tooltip.style.opacity = '1'
                }
            })
            
            indicator.addEventListener('mouseleave', () => {
                if (!isResizing) {
                    indicator.style.background = currentHidden[index] ? 
                        'rgba(255, 107, 107, 0.1)' : 
                        (border ? 'rgba(230, 234, 241, 0.1)' : 'rgba(100, 100, 100, 0.05)')
                    label.style.opacity = currentHidden[index] ? '0.8' : '0.7'
                    tooltip.style.opacity = '0'
                }
            })
            
            // Double-click to hide/show column
            let clickCount = 0
            let clickTimer = null
            
            indicator.addEventListener('click', () => {
                clickCount++
                if (clickCount === 1) {
                    clickTimer = setTimeout(() => {
                        clickCount = 0
                    }, 300)
                } else if (clickCount === 2) {
                    clearTimeout(clickTimer)
                    clickCount = 0
                    
                    // Toggle hidden state
                    currentHidden[index] = !currentHidden[index]
                    
                    // Send updated hidden state to Streamlit
                    Streamlit.setComponentValue({
                        widths: currentWidths,
                        hidden: currentHidden,
                        action: "toggle_hidden"
                    })
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
        indicators.forEach((indicator, index) => {
            indicator.style.background = currentHidden[index] ? 
                'rgba(255, 107, 107, 0.1)' : 
                (border ? 'rgba(230, 234, 241, 0.1)' : 'rgba(100, 100, 100, 0.05)')
            const label = indicator.querySelector('div')
            if (label) label.style.opacity = currentHidden[index] ? '0.8' : '0.7'
        })
        
        // Send updated widths back to Streamlit
        Streamlit.setComponentValue({
            widths: currentWidths,
            hidden: currentHidden,
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