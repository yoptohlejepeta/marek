local Color = require("src.ui.colors")
local Button = require("src.ui.button")
local fileUtils = require("src.file_utils")

---@class Sidebar
---@field elements Button[]
local Sidebar = { elements = {} }

function Sidebar:new()
  local obj = setmetatable({}, self)
  self.__index = self
  obj.elements = {}

  return obj
end

function Sidebar:draw()
  local _, height = love.window.getDesktopDimensions()
  local width = love.graphics.getWidth() * 0.15

  love.graphics.setColor(Color.CRUST)
  love.graphics.rectangle("fill", 0, 0, width, height)

  for _, element in ipairs(self.elements) do
    element:draw()
  end
end

function Sidebar:update()
  for _, element in pairs(self.elements) do
    element:update()
  end
end

return Sidebar
