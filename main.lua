local Sidebar = require("src.ui.sidebar")
local Color = require("src.ui.colors")

function love.load()
	love.window.maximize()
	local font = love.graphics.newFont(16)
	love.graphics.setFont(font)
	love.graphics.setBackgroundColor(Color.BASE)

	Lines = {}
	CurrentLine = nil
	AppSidebar = Sidebar:new()
end

function love.update(dt)
	AppSidebar:update()
	if love.mouse.isDown(1) then
		local mx, my = love.mouse.getPosition()

		if mx > 200 then
			if CurrentLine then
				local prevX = CurrentLine[#CurrentLine - 1]
				local prevY = CurrentLine[#CurrentLine]

				if math.abs(mx - prevX) > 2 or math.abs(my - prevY) > 2 then
					table.insert(CurrentLine, mx)
					table.insert(CurrentLine, my)
				end
			end
		end
	end
end

function love.mousepressed(x, y, button)
	if button == 1 and x > 200 then
		CurrentLine = { x, y }
		table.insert(Lines, CurrentLine)
	end
end

function love.mousereleased(x, y, button)
	if button == 1 then
		CurrentLine = nil
	end
end

function love.draw()
	love.graphics.setColor(1, 1, 1) -- Set brush color (White)
	love.graphics.setLineWidth(5)
	love.graphics.setLineJoin("none") -- Makes jagged lines smoother

	for _, line in ipairs(Lines) do
		-- We need at least 4 coordinates (2 points) to draw a segment
		if #line >= 4 then
			love.graphics.line(line)
		end
	end

	AppSidebar:draw()
end
