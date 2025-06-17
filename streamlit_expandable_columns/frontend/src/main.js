// Import Streamlit's component base
import { Streamlit } from "streamlit-component-lib"

/**
 * The component's main function
 */
function onRender(event) {
    const data = event.detail
    const config = data.args.config
    const widths = config.widths
    const labels = config.labels || widths.map((_, i) => `Col ${i+1}`)
    
    // Hardcoded minimum width: 6% for all columns
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
    
    // Get Streamlit theme colors with better defaults
    const theme = {
        primary: getComputedStyle(document.documentElement).getPropertyValue('--primary-color') || '#ff6b6b',
        background: getComputedStyle(document.documentElement).getPropertyValue('--background-color') || '#ffffff',
        secondary: getComputedStyle(document.documentElement).getPropertyValue('--secondary-background-color') || '#f0f2f6',
        text: getComputedStyle(document.documentElement).getPropertyValue('--text-color') || '#262730',
        border: getComputedStyle(document.documentElement).getPropertyValue('--border-color') || '#e6eaf1'
    }
    
    // Create the control bar - match exact column layout with proper borders
    const controlBar = document.createElement("div")
    controlBar.style.cssText = `
        display: flex;
        height: 24px;
        width: 100%;
        margin: 0;
        padding: 0;
        background: ${theme.secondary};
        border: 1px solid ${theme.border || theme.text + '20'};
        border-radius: 4px;
        overflow: hidden;
        user-select: none;
        box-sizing: border-box;
    `
    
    // Calculate total width and account for gaps like Streamlit does
    const totalWidth = currentWidths.reduce((sum, w) => sum + w, 0)
    
    // Create segments that exactly match Streamlit column proportions
    currentWidths.forEach((width, index) => {
        // Column segment - adjust for gap spacing to align with actual column boundaries
        const segment = document.createElement("div")
        
        // Calculate the effective width accounting for gaps
        // Streamlit adds gaps between columns, so we need to adjust our segments
        const widthPercentage = (width / totalWidth) * 100
        const gapAdjustment = index === 0 ? 0 : 0.5  // Small adjustment for gap alignment
        const adjustedWidth = `calc(${widthPercentage}% - ${gapAdjustment}px)`
        
        segment.style.cssText = `
            width: ${adjustedWidth};
            flex-shrink: 0;
            height: 100%;
            background: ${theme.background};
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: ${theme.text};
            font-weight: 600;
            transition: background-color 0.15s ease;
            text-overflow: ellipsis;
            white-space: nowrap;
            overflow: hidden;
            padding: 0 6px;
            box-sizing: border-box;
            margin: 0;
            outline: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        `
        
        // Add borders to create proper segments - all segments get right border except container handles the outer border
        if (index < currentWidths.length - 1) {
            segment.style.borderRight = `1px solid ${theme.border || theme.text + '20'}`
        }
        
        segment.textContent = labels[index]
        segment.title = labels[index] // Tooltip for long labels
        
        // Subtle hover effect - no gradients
        segment.addEventListener('mouseenter', () => {
            segment.style.background = theme.secondary
        })
        segment.addEventListener('mouseleave', () => {
            segment.style.background = theme.background
        })
        
        // Add resize handle (except for last segment)
        if (index < currentWidths.length - 1) {
            const handle = document.createElement("div")
            handle.style.cssText = `
                position: absolute;
                right: -2px;
                top: 2px;
                width: 4px;
                height: calc(100% - 4px);
                background: ${theme.text}40;
                cursor: col-resize;
                z-index: 10;
                border-radius: 2px;
                transition: all 0.15s ease;
            `
            handle.dataset.index = index
            handle.addEventListener('mousedown', startResize)
            
            // Visual feedback
            handle.addEventListener('mouseenter', () => {
                handle.style.background = theme.primary
                handle.style.width = '6px'
                handle.style.right = '-3px'
            })
            handle.addEventListener('mouseleave', () => {
                handle.style.background = `${theme.text}40`
                handle.style.width = '4px'
                handle.style.right = '-2px'
            })
            
            segment.appendChild(handle)
        }
        
        controlBar.appendChild(segment)
    })
    
    container.appendChild(controlBar)
    
    function startResize(e) {
        isResizing = true
        startX = e.clientX
        resizingIndex = parseInt(e.target.dataset.index)
        startWidths = [...currentWidths]
        
        e.target.style.background = theme.primary
        e.target.style.width = '6px'
        e.target.style.right = '-3px'
        document.addEventListener('mousemove', resize)
        document.addEventListener('mouseup', stopResize)
        
        e.preventDefault()
    }
    
    function resize(e) {
        if (!isResizing) return
        
        const deltaX = e.clientX - startX
        const barWidth = controlBar.offsetWidth
        const totalCurrentWidth = currentWidths.reduce((sum, w) => sum + w, 0)
        
        // Calculate change in ratio
        const deltaRatio = (deltaX / barWidth) * totalCurrentWidth
        
        const leftIndex = resizingIndex
        const rightIndex = resizingIndex + 1
        
        // Apply minimum constraints using the actual minimum width ratios
        const leftMin = MIN_WIDTH_RATIO * totalCurrentWidth
        const rightMin = MIN_WIDTH_RATIO * totalCurrentWidth
        
        let newLeftWidth = Math.max(leftMin, startWidths[leftIndex] + deltaRatio)
        let newRightWidth = Math.max(rightMin, startWidths[rightIndex] - deltaRatio)
        
        // Ensure we don't violate minimums with proper constraint handling
        if (newLeftWidth < leftMin) {
            newLeftWidth = leftMin
            newRightWidth = startWidths[rightIndex] + (startWidths[leftIndex] - leftMin)
        }
        if (newRightWidth < rightMin) {
            newRightWidth = rightMin
            newLeftWidth = startWidths[leftIndex] + (startWidths[rightIndex] - rightMin)
        }
        
        // Final check: ensure both columns respect their minimums
        newLeftWidth = Math.max(newLeftWidth, leftMin)
        newRightWidth = Math.max(newRightWidth, rightMin)
        
        currentWidths[leftIndex] = newLeftWidth
        currentWidths[rightIndex] = newRightWidth
        
        // Update visual using the adjusted width calculation
        updateBar()
    }
    
    function updateBar() {
        const newTotal = currentWidths.reduce((sum, w) => sum + w, 0)
        const segments = controlBar.children
        
        for (let i = 0; i < segments.length; i++) {
            // Recalculate adjusted width for each segment
            const widthPercentage = (currentWidths[i] / newTotal) * 100
            const gapAdjustment = i === 0 ? 0 : 0.5
            const adjustedWidth = `calc(${widthPercentage}% - ${gapAdjustment}px)`
            segments[i].style.width = adjustedWidth
        }
    }
    
    function stopResize(e) {
        if (!isResizing) return
        
        isResizing = false
        document.removeEventListener('mousemove', resize)
        document.removeEventListener('mouseup', stopResize)
        
        // Reset handle appearance
        const handles = controlBar.querySelectorAll('[data-index]')
        handles.forEach(handle => {
            handle.style.background = `${theme.text}40`
            handle.style.width = '4px'
            handle.style.right = '-2px'
        })
        
        // Send updated widths back to Streamlit
        Streamlit.setComponentValue({
            widths: currentWidths,
            action: "resize"
        })
    }
    
    // Set minimal height
    Streamlit.setFrameHeight(30)
}

// Attach our function to the onRender event
Streamlit.events.addEventListener("streamlit:render", onRender)

// Tell Streamlit we're ready to receive data
Streamlit.setComponentReady() 