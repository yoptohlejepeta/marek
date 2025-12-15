---@class Polygon
---@field points number[] x,y pairs in image coordinates
---@field colorIdx integer index into colors array
---@field closed boolean whether polygon is closed

---@class Annotations
---@field imageAnnotations table<integer, Polygon[]> annotations per image index
---@field currentPolygon Polygon? current polygon being drawn
---@field currentImageIdx integer? image index of current polygon
---@field closeThreshold number distance threshold to close polygon
---@field colors table[] array of colors to rotate through
local Annotations = {
  imageAnnotations = {},
  currentPolygon = nil,
  currentImageIdx = nil,
  closeThreshold = 15,
  colors = {
    { 1,   0.4, 0.4 },
    { 0.4, 1,   0.4 },
    { 0.4, 0.4, 1 },
    { 1,   1,   0.4 },
    { 1,   0.4, 1 },
  }
}

function Annotations:new()
  local obj = setmetatable({}, self)
  self.__index = self
  obj.imageAnnotations = {}
  obj.currentPolygon = nil
  obj.currentImageIdx = nil
  return obj
end

function Annotations:getNextColorIdx(imageIdx)
  local polygons = self.imageAnnotations[imageIdx]
  if not polygons or #polygons == 0 then
    return 1
  end
  return (#polygons % #self.colors) + 1
end

function Annotations:startPolygon(imageIdx, imgX, imgY)
  if not self.imageAnnotations[imageIdx] then
    self.imageAnnotations[imageIdx] = {}
  end
  self.currentImageIdx = imageIdx
  self.currentPolygon = {
    points = { imgX, imgY },
    colorIdx = self:getNextColorIdx(imageIdx),
    closed = false
  }
  table.insert(self.imageAnnotations[imageIdx], self.currentPolygon)
end

function Annotations:addPoint(imgX, imgY)
  if self.currentPolygon then
    local points = self.currentPolygon.points
    local prevX = points[#points - 1]
    local prevY = points[#points]
    if math.abs(imgX - prevX) > 1 or math.abs(imgY - prevY) > 1 then
      table.insert(points, imgX)
      table.insert(points, imgY)
    end
  end
end

function Annotations:endPolygon()
  if not self.currentPolygon or not self.currentImageIdx then
    self.currentPolygon = nil
    self.currentImageIdx = nil
    return
  end

  local points = self.currentPolygon.points
  if #points >= 6 then
    local startX, startY = points[1], points[2]
    local endX, endY = points[#points - 1], points[#points]
    local dist = math.sqrt((endX - startX) ^ 2 + (endY - startY) ^ 2)

    if dist <= self.closeThreshold then
      self.currentPolygon.closed = true
      self.currentPolygon = nil
      self.currentImageIdx = nil
      return
    end
  end

  local polygons = self.imageAnnotations[self.currentImageIdx]
  for i, poly in ipairs(polygons) do
    if poly == self.currentPolygon then
      table.remove(polygons, i)
      break
    end
  end

  self.currentPolygon = nil
  self.currentImageIdx = nil
end

function Annotations:draw(imageIdx, transform)
  local polygons = self.imageAnnotations[imageIdx]
  if not polygons then return end

  love.graphics.setLineWidth(5)
  love.graphics.setLineJoin("miter")

  for _, polygon in ipairs(polygons) do
    local points = polygon.points
    if #points >= 4 then
      local screenPoints = {}
      for i = 1, #points, 2 do
        local imgX, imgY = points[i], points[i + 1]
        local screenX = transform.x + imgX * transform.scale
        local screenY = transform.y + imgY * transform.scale
        table.insert(screenPoints, screenX)
        table.insert(screenPoints, screenY)
      end

      local color = self.colors[polygon.colorIdx]

      if polygon.closed and #screenPoints >= 6 then
        love.graphics.setColor(color[1], color[2], color[3], 0.3)
        local ok, triangles = pcall(love.math.triangulate, screenPoints)
        if ok then
          for _, tri in ipairs(triangles) do
            love.graphics.polygon("fill", tri)
          end
        end
        love.graphics.setColor(color[1], color[2], color[3], 1)
        love.graphics.polygon("line", screenPoints)
      else
        love.graphics.setColor(color[1], color[2], color[3], 1)
        love.graphics.line(screenPoints)
      end
    end
  end
end

function Annotations:save()
  -- print(unpack(self.imageAnnotations))
  for _, ann in pairs(self.imageAnnotations) do
    print(unpack(ann))
  end
end

return Annotations
