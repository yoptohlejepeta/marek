local Sidebar = require("src.ui.sidebar")
local Color = require("src.ui.colors")

love.window.maximize()

function love.load()
	local font = love.graphics.newFont(16)
	love.graphics.setFont(font)
	love.graphics.setBackgroundColor(Color.BASE)
end

function love.update(dt) end

function love.draw()
	Sidebar:draw()
end
