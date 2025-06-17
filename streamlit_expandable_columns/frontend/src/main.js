// Import Streamlit's component base
import { Streamlit } from "streamlit-component-lib"

/**
 * The component's main function
 */
function onRender(event) {
    const data = event.detail
    const config = data.args.config
    const widths = config.widths
    const minWidths = config.min_widths || widths.map(() => 0.1)
    
    // Create the container
    const container = document.getElementById("root")
    container.innerHTML = ""
    
    const columnsContainer = document.createElement("div")
    columnsContainer.className = "resizable-columns-container"
    
    // Calculate percentages
    const totalWidth = widths.reduce((sum, w) => sum + w, 0)
    const percentages = widths.map(w => (w / totalWidth) * 100)
    
    // Store current state
    let currentWidths = [...widths]
    let isResizing = false
    let startX = 0
    let startWidths = []
    let resizingIndex = -1
    
    // Create columns
    widths.forEach((width, index) => {
        const column = document.createElement("div")
        column.className = "column"
        column.style.width = `${percentages[index]}%`
        
        const label = document.createElement("div")
        label.className = "column-label"
        label.textContent = `Col ${index + 1}`
        column.appendChild(label)
        
        // Add resizer (except for last column)
        if (index < widths.length - 1) {
            const resizer = document.createElement("div")
            resizer.className = "resizer"
            resizer.dataset.index = index
            
            resizer.addEventListener("mousedown", startResize)
            column.appendChild(resizer)
        }
        
        columnsContainer.appendChild(column)
    })
    
    container.appendChild(columnsContainer)
    
    // Resize functionality
    function startResize(e) {
        isResizing = true
        startX = e.clientX
        resizingIndex = parseInt(e.target.dataset.index)
        startWidths = [...currentWidths]
        
        e.target.classList.add("active")
        document.addEventListener("mousemove", resize)
        document.addEventListener("mouseup", stopResize)
        
        e.preventDefault()
    }
    
    function resize(e) {
        if (!isResizing) return
        
        const deltaX = e.clientX - startX
        const containerWidth = columnsContainer.offsetWidth
        const totalCurrentWidth = currentWidths.reduce((sum, w) => sum + w, 0)
        
        // Calculate the change in ratio
        const deltaRatio = (deltaX / containerWidth) * totalCurrentWidth
        
        // Update widths
        const newWidths = [...startWidths]
        const leftIndex = resizingIndex
        const rightIndex = resizingIndex + 1
        
        // Calculate minimum widths in ratio terms
        const leftMinRatio = minWidths[leftIndex] * totalCurrentWidth
        const rightMinRatio = minWidths[rightIndex] * totalCurrentWidth
        
        // Apply changes with constraints
        const newLeftWidth = Math.max(leftMinRatio, startWidths[leftIndex] + deltaRatio)
        const newRightWidth = Math.max(rightMinRatio, startWidths[rightIndex] - deltaRatio)
        
        // Ensure the total doesn't change significantly
        const totalChange = (newLeftWidth - startWidths[leftIndex]) + (newRightWidth - startWidths[rightIndex])
        if (Math.abs(totalChange) > 0.001) {
            // Adjust to maintain total
            const adjustment = totalChange / 2
            newWidths[leftIndex] = newLeftWidth - adjustment
            newWidths[rightIndex] = newRightWidth + adjustment
        } else {
            newWidths[leftIndex] = newLeftWidth
            newWidths[rightIndex] = newRightWidth
        }
        
        // Update current widths
        currentWidths = newWidths
        
        // Update visual representation
        const newTotal = currentWidths.reduce((sum, w) => sum + w, 0)
        const columns = columnsContainer.children
        
        for (let i = 0; i < currentWidths.length; i++) {
            const percentage = (currentWidths[i] / newTotal) * 100
            columns[i].style.width = `${percentage}%`
        }
    }
    
    function stopResize(e) {
        if (!isResizing) return
        
        isResizing = false
        const activeResizer = document.querySelector(".resizer.active")
        if (activeResizer) {
            activeResizer.classList.remove("active")
        }
        
        document.removeEventListener("mousemove", resize)
        document.removeEventListener("mouseup", stopResize)
        
        // Send updated widths back to Streamlit
        Streamlit.setComponentValue({
            widths: currentWidths,
            action: "resize"
        })
    }
    
    // Set initial height
    Streamlit.setFrameHeight(50)
}

// Attach our function to the onRender event
Streamlit.events.addEventListener("streamlit:render", onRender)

// Tell Streamlit we're ready to receive data
Streamlit.setComponentReady() 