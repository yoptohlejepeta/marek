local Color = require("src.ui.colors")
local Button = require("src.ui.button")

---@class Sidebar
local Sidebar = {}

function Sidebar.draw()
	local _, height = love.window.getDesktopDimensions()
	local width = love.graphics.getWidth()

	love.graphics.setColor(Color.CRUST)
	love.graphics.rectangle("fill", 0, 0, width * 0.15, height)

	Button:new({ x = 20, y = 20, text = "Button" }):draw()
end

return Sidebar
